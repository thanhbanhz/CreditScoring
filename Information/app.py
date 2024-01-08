from flask import Flask, jsonify, render_template, request
from user_agents import parse

app = Flask(__name__, template_folder="../templates")

app.config['DEBUG'] = True
app.config['HOST'] = '0.0.0.0'

def get_device_info(user_agent):
    user_agent_data = parse(user_agent)
    device_info = {
        'system': user_agent_data.os.family,
        'release': user_agent_data.os.version_string,
        'version': user_agent_data.browser.version_string,
        'machine': user_agent_data.device.family,
        'browser': user_agent_data.browser.family,
    }
    return device_info

@app.route("/")
@app.route('/index')
def index():
    user_agent = request.headers.get('User-Agent')
    device_info = get_device_info(user_agent)
    return render_template('index.html', device_info=device_info)

@app.route('/get_ip', methods=['GET'])
def get_ip():
    ip_address = request.remote_addr
    network_ip_address = request.environ['REMOTE_ADDR']
    user_agent = request.headers.get('User-Agent')
    device_info = get_device_info(user_agent)
    
    return jsonify({'ip_address': ip_address, 'network_ip_address': network_ip_address, 'device_info': device_info})

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        # Xử lý thông tin đăng ký
        full_name = request.form['fullName']
        birth_date = request.form['birthDate']
        gender = request.form['gender']
        id_card = request.form['idCard']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        current_address = request.form['currentAddress']
        occupation = request.form['occupation']
        workplace = request.form['workplace']
        monthly_income = request.form['monthlyIncome']

        # Hiển thị thông tin máy truy cập
        user_agent = request.headers.get('User-Agent')
        ip_address = request.remote_addr
        network_ip_address = request.environ['REMOTE_ADDR']
        device_info = get_device_info(user_agent)

        return render_template('result.html', 
                       full_name=full_name, birth_date=birth_date, gender=gender, id_card=id_card,
                       phone=phone, email=email, address=address, current_address=current_address,
                       occupation=occupation, workplace=workplace, monthly_income=monthly_income,
                       user_agent=user_agent, ip_address=ip_address, network_ip_address=network_ip_address,
                       device_info=device_info)

if __name__ == '__main__':
    app.run(debug=True, host=app.config['HOST'])
