from flask import Flask, request, jsonify, render_template
import subprocess, tempfile, os, stat

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_elf():
    try:
        # Get the uploaded file
        file = request.files['elfFile']
        if not file:
            return jsonify({'error': 'No file uploaded'}), 400
        
        # Save to a unique temporary directory
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, 'uploaded_elf')
        
        try:
            # Save the uploaded file
            file.save(temp_path)
            
            # Make the file executable
            os.chmod(temp_path, stat.S_IRWXU)
            
            # Execute the ELF file with a timeout
            result = subprocess.run(
                [temp_path],
                capture_output=True,
                text=True,
                timeout=600,
                cwd=temp_dir
            )
            
            output = {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
            return jsonify(output)
            
        except subprocess.TimeoutExpired:
            return jsonify({'error': 'Execution timed out'}), 408
        except Exception as e:
            return jsonify({'error': f'Execution failed: {str(e)}'}), 500
        finally:
            # Clean up the entire temporary directory
            import shutil
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass  # Let the OS clean it up later if needed
                
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
