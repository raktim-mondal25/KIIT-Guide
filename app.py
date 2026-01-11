from flask import Flask, send_file, jsonify, request, send_from_directory
import os
import json
import io
import qrcode
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

# Configuration from your index.html
CONFIG = {
    'firebase': {
        'apiKey': "AIzaSyAvdVw_yOQtxvSd9MTU_hRz1AD6RDCaQ0A",
        'authDomain': "navigator-4a29d.firebaseapp.com",
        'projectId': "navigator-4a29d",
        'storageBucket': "navigator-4a29d.firebasestorage.app",
        'messagingSenderId': "670551267892",
        'appId': "1:670551267892:web:3c7f7a66c53f262adcc861"
    },
    'admin_email': "riddhipdas@gmail.com",
    'map_key': "1DAJJ44xYcqv8JcwhP0L"
}

# Preloaded places data from your index.html
PRELOADED_PLACES = [
    {"name": "Campus 3 Academic Block", "type": "academic", "lat": 20.352761729599813, "lng": 85.81724230083005},
    {"name": "Campus 7 Academic Block", "type": "academic", "lat": 20.350520271622248, "lng": 85.82070018739302},
    {"name": "Campus 8 Academic Block", "type": "academic", "lat": 20.35099617352404, "lng": 85.82057163453852},
    {"name": "Campus 12 Academic Block", "type": "academic", "lat": 20.355359600371553, "lng": 85.82056452901325},
    {"name": "Campus 14 Academic Block", "type": "academic", "lat": 20.35540833201611, "lng": 85.81515308787915},
    {"name": "Campus 15 Academic Block", "type": "academic", "lat": 20.3483529749744, "lng": 85.81614386130093},
    {"name": "Campus 16 Academic Block", "type": "academic", "lat": 20.362074804798052, "lng": 85.8229493340014},
    {"name": "Campus 17 Academic Block", "type": "academic", "lat": 20.349114232934372, "lng": 85.81956979349994},
    {"name": "Campus 25 Academic Block", "type": "academic", "lat": 20.36455929074428, "lng": 85.81730592511482},
    {"name": "King's Palace 1", "type": "hostel", "lat": 20.35440136062493, "lng": 85.82021742698775},
    {"name": "King's Palace 2", "type": "hostel", "lat": 20.354766719102646, "lng": 85.81905247116465},
    {"name": "King's Palace 3", "type": "hostel", "lat": 20.354458601632377, "lng": 85.81947044232925},
    {"name": "King's Palace 5", "type": "hostel", "lat": 20.356873000543768, "lng": 85.82012030142747},
    {"name": "King's Palace 5A", "type": "hostel", "lat": 20.356437661562104, "lng": 85.81996552173172},
    {"name": "King's Palace 6-AB", "type": "hostel", "lat": 20.348880242653706, "lng": 85.8161307198512},
    {"name": "King's Palace 6-C", "type": "hostel", "lat": 20.348739412708504, "lng": 85.81682809422018},
    {"name": "King's Palace 7-AB", "type": "hostel", "lat": 20.351971848844183, "lng": 85.81605489341933},
    {"name": "King's Palace 8-A", "type": "hostel", "lat": 20.360370203376362, "lng": 85.82370951586763},
    {"name": "King's Palace 8-c", "type": "hostel", "lat": 20.36081906457951, "lng": 85.82299336608033},
    {"name": "King's Palace 9-D", "type": "hostel", "lat": 20.34960382820302, "lng": 85.8155381074431},
    {"name": "King's Palace 10-A", "type": "hostel", "lat": 20.354503690053704, "lng": 85.81664690571996},
    {"name": "King's Palace 10-B", "type": "hostel", "lat": 20.354679255226507, "lng": 85.81633128211355},
    {"name": "King's Palace 12", "type": "hostel", "lat": 20.35200319910663, "lng": 85.82138055016974},
    {"name": "King's Palace 25-A,B,C,D", "type": "hostel", "lat": 20.364095139563137, "lng": 85.81613756366418},
    {"name": "Queen's Castle 1", "type": "hostel", "lat": 20.352478588914085, "lng": 85.81809212225603},
    {"name": "Queen's Castle 2", "type": "hostel", "lat": 20.352337129057517, "lng": 85.8187784533921},
    {"name": "Queen's Castle 3", "type": "hostel", "lat": 20.352381655841935, "lng": 85.81700301726396},
    {"name": "Queen's Castle 4", "type": "hostel", "lat": 20.3525538643575, "lng": 85.81827559094287},
    {"name": "Central Library", "type": "library", "lat": 20.354055008292377, "lng": 85.81637333664973},
    {"name": "KIMS Library", "type": "library", "lat": 20.353580445182, "lng": 85.8155388716826},
    {"name": "Campus 15 Library", "type": "library", "lat": 20.348526388447393, "lng": 85.81612493499773},
    {"name": "Campus 25 Library", "type": "library", "lat": 20.363722616110923, "lng": 85.81718221225094},
    {"name": "KIIT School of Management Library", "type": "library", "lat": 20.349987111740095, "lng": 85.82074640735456},
    {"name": "KIIT Cricket Field", "type": "sports", "lat": 20.357353810053166, "lng": 85.81794109873883},
    {"name": "KIIT Indoor Stadium", "type": "sports", "lat": 20.357233105301212, "lng": 85.81893351604296},
    {"name": "KIIT Outdoor Football Stadium", "type": "sports", "lat": 20.358537630508575, "lng": 85.81774003304848},
    {"name": "KIIT Hockey Stadium", "type": "sports", "lat": 20.35876394992908, "lng": 85.81684953968367},
    {"name": "KIIT Palace 5 ground", "type": "sports", "lat": 20.35691676769393, "lng": 85.81959422026844},
    {"name": "Campus 1", "type": "admin", "lat": 20.346234153476026, "lng": 85.82354974079325},
    {"name": "Campus 4", "type": "admin", "lat": 20.35380253557167, "lng": 85.81989100774194},
]

# Personnel data from your index.html
PERSONNEL = [
    {
        "title": "Director General",
        "name": "Prof. Sasmita Samanta",
        "office": "Campus 3, Administrative Block",
        "room": "DG Office, 3rd Floor",
        "campus": "Campus 3",
        "phone": "0674-272-7777",
        "lat": 20.3555,
        "lng": 85.8188
    },
    {
        "title": "Dean - School of Computer Engineering",
        "name": "Prof. Amiya Kumar Rath",
        "office": "Campus 3",
        "room": "Room 301, CS Building",
        "campus": "Campus 3",
        "phone": "0674-272-8888",
        "lat": 20.3555,
        "lng": 85.8188
    },
    {
        "title": "Dean - Student Welfare",
        "name": "Prof. Jnyana Ranjan Mohanty",
        "office": "Campus 1, Student Activity Center",
        "room": "DSW Office, 2nd Floor",
        "campus": "Campus 1",
        "phone": "0674-272-9999",
        "lat": 20.354055,
        "lng": 85.816373
    },
    {
        "title": "Registrar",
        "name": "Dr. Mrutyunjay Suar",
        "office": "Campus 3, Administrative Block",
        "room": "Registrar Office, 2nd Floor",
        "campus": "Campus 3",
        "phone": "0674-272-6666",
        "lat": 20.3555,
        "lng": 85.8188
    },
    {
        "title": "Dean - School of Management",
        "name": "Prof. Biswajit Satpathy",
        "office": "KIIT School of Management",
        "room": "Dean Office, KSOM Building",
        "campus": "Campus 7",
        "phone": "0674-272-5555",
        "lat": 20.349987,
        "lng": 85.820746
    }
]

@app.route('/')
def home():
    """Serve the main HTML page"""
    return send_file('index.html')

@app.route('/api/config')
def get_config():
    """Return Firebase configuration"""
    return jsonify(CONFIG)

@app.route('/api/places')
def get_places():
    """Get all places"""
    return jsonify(PRELOADED_PLACES)

@app.route('/api/personnel')
def get_personnel():
    """Get all personnel"""
    return jsonify(PERSONNEL)

@app.route('/api/search')
def search():
    """Search for places and personnel"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify([])
    
    results = []
    
    # Search in places
    for place in PRELOADED_PLACES:
        if (query in place['name'].lower() or 
            query in place['type'].lower()):
            results.append({
                **place,
                'kind': 'place',
                'display': place['name'],
                'type': place['type']
            })
    
    # Search in personnel
    for person in PERSONNEL:
        if (query in person['name'].lower() or 
            query in person['title'].lower() or
            query in person['office'].lower()):
            results.append({
                **person,
                'kind': 'person',
                'display': person['title'],
                'name': person['name']
            })
    
    return jsonify(results[:10])  # Return top 10 results

@app.route('/api/generate_qr')
def generate_qr():
    """Generate QR code"""
    url = request.args.get('url', request.host_url)
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to bytes
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'KIIT Connect Flask API',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    if os.path.exists(filename):
        return send_file(filename)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f" Starting KIIT Connect Flask Server...")
    print(f"Directory: {os.getcwd()}")
    print(f"Server: http://localhost:{port}")
    print(f"API Endpoints:")
    print(f"   GET  /api/config     - Get Firebase configuration")
    print(f"   GET  /api/places     - Get all places")
    print(f"   GET  /api/personnel  - Get all personnel")
    print(f"   GET  /api/search?q=  - Search places/personnel")
    print(f"   GET  /api/generate_qr?url= - Generate QR code")
    print(f"   GET  /api/health     - Health check")
    print("-" * 50)
    app.run(host='0.0.0.0', port=port, debug=True)