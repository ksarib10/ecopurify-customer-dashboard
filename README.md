# EcoPurify Customer Dashboard

A production-grade **customer dashboard** for managing RO (Reverse Osmosis) water plants, built for a real client.

---

## 🔥 Features

- Customer login with session-based authentication
- One customer → multiple RO plants
- Sidebar-based plant switching
- Live service status monitoring
- Automatic health degradation based on service date
- Google Sheets as the backend database
- Mobile-responsive UI
- Real-time clock & live indicators

---

## 🧱 Tech Stack

### Backend
- Python
- Flask
- gspread
- Google Service Account

### Frontend
- HTML5
- CSS3 (Responsive, mobile-first)
- Vanilla JavaScript

### Database
- Google Sheets

---

## 📊 Health Degradation Logic

Health is calculated using **days since last service**:

| Days Passed | Health Status |
|------------|--------------|
| < 35       | Excellent |
| ≥ 35       | Good |
| ≥ 45       | Average |
| ≥ 60       | Needs Attention |

Health is automatically:
- Updated in **Google Sheets**
- Reflected on the **dashboard UI**

Triggered via `/refresh`.

---

## 📁 Project Structure

app/
├── app.py # Flask routes & session logic
├── utils.py # Date parsing & health logic
├── auth_service.py # Authentication
├── sheets.py # Google Sheets helpers
├── static/
│ ├── css/style.css
│ ├── js/login.js
│ ├── js/dashboard.js
│ └── images/
├── templates/
│ ├── login.html
│ └── dashboard.html
credentials/
requirements.txt

---

## 🔐 Authentication Flow

1. User logs in with `customer_id + password`
2. All plants linked to that customer are loaded
3. First plant is set as active by default
4. Active plant stored in session
5. Sidebar used to switch plants dynamically

---

## 🚀 Running Locally

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python app/app.py



📝 Notes

- This is a real client project
- Google Sheet is managed manually by admin
- Health logic is fully time-based
- Code prioritizes clarity & maintainability


👤 Author

Developed by Sarib Yar Khan
For EcoPurify