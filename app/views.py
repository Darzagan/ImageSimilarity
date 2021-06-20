# Important imports
from app import app
from flask import request, render_template, send_from_directory
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image

# Adding path to config
app.config['IMAGE1_UPLOAD'] = 'app/static/upload1'
app.config['IMAGE2_UPLOAD'] = 'app/static/upload2'


# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():

	# Execute if request is get
	if request.method == "GET":
	    return render_template("index.html")

	# Execute if reuqest is post
	if request.method == "POST":
                # Get uploaded image
                image1_upload = request.files['image1_upload']
                image1name = image1_upload.filename
                image2_upload = request.files['image2_upload']
                image2name = image2_upload.filename
                
                # Resize and save the uploaded image
                uploaded_image1 = Image.open(image1_upload).resize((250,160))
                uploaded_image1.save(os.path.join(app.config['IMAGE1_UPLOAD'], 'image.jpg'))
                uploaded_image2 = Image.open(image2_upload).resize((250,160))
                uploaded_image2.save(os.path.join(app.config['IMAGE2_UPLOAD'], 'image.jpg'))

                # Read image1 and image2 as array
                uploaded_image1 = cv2.imread(os.path.join(app.config['IMAGE1_UPLOAD'], 'image.jpg'))
                uploaded_image2 = cv2.imread(os.path.join(app.config['IMAGE2_UPLOAD'], 'image.jpg'))

                # Convert image into grayscale
                image1_gray = cv2.cvtColor(uploaded_image1, cv2.COLOR_BGR2GRAY)
                image2_gray = cv2.cvtColor(uploaded_image2, cv2.COLOR_BGR2GRAY)

                # Calculate structural similarity
                (score, diff) = structural_similarity(image1_gray, image2_gray, full=True)
                # diff = (diff * 255).astype("uint8")

                # # Save all output images (if required)
                # cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
                # cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
                # cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
                # cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)
                image1_path = os.path.join(app.config['IMAGE1_UPLOAD'], 'image.jpg')
                return render_template('output.html', image1_path = image1_path, pred=  str(image1name[:len(image1name)-4]) + ' and ' + str(image2name[:len(image2name)-4])+ ' are ' + str(score) + '%' + ' close')

                # return render_template('index.html',pred=str(round(score*100,2)) + '%' + ' correct')
       
# Main function
if __name__ == '__main__':
    app.run(debug=True)
