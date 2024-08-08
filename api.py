from flask import Flask, request, jsonify, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    try:
        # Get data from the request
        data = request.json.get('data', '')

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill='black', back_color='white')

        # Save the image to a BytesIO object
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Send the image back as a response
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
