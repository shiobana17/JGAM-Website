from flask import Flask, jsonify, Response
from flask_cors import CORS
import os
from typing import List, Dict, Any # Import types for hinting

app = Flask(__name__)
CORS(app)

# The root directory for your gallery images, relative to this script
GALLERY_DIR = os.path.join('..', 'frontend', 'images')

@app.route('/api/gallery')
def get_gallery_data() -> Response:
    """
    Scans the gallery directory and builds a JSON structure of the albums,
    ignoring any images in the root 'images' folder.
    """
    albums: List[Dict[str, Any]] = []
    
    # os.walk traverses the directory tree top-down
    for root, dirs, files in os.walk(GALLERY_DIR):
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            continue # Skip this directory if it has no images

        relative_path = os.path.relpath(root, GALLERY_DIR)
        
        if relative_path != '.':
            # Create a user-friendly album name from the folder path
            album_name = relative_path.replace(os.path.sep, ' / ').title()

            # Create a list of web-accessible paths for each image
            image_paths = [os.path.join('images', relative_path, f).replace('\\', '/') for f in image_files]
            
            album_data: Dict[str, Any] = {
                "albumName": album_name,
                "coverImage": image_paths[0], # Use the first image as the cover
                "images": image_paths,
                "captions": [f"Image {i+1} from {album_name}" for i in range(len(image_paths))] # Dynamic captions
            }
            albums.append(album_data)

    return jsonify(albums)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

