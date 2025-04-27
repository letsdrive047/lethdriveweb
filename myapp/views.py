from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import logging
from firebase_admin import firestore,auth,credentials,storage
import firebase_admin
from django.http import JsonResponse
from .forms import EmployeeRegistrationForm
from django.views.decorators.csrf import csrf_exempt
from .decorators import role_required
from django.http import HttpResponseForbidden

# Initialize Firestore
logging.basicConfig(level=logging.INFO)
db = firestore.client()



def driver_dashboard(request):
    uid = request.session.get('employee_uid')
    if not uid:
        return redirect('driver_login')  # Redirect if employee_uid is not in session

    employee_ref = db.collection('employees').document(uid).get()
    if not employee_ref.exists:
        return redirect('driver_login')  # Redirect if employee doesn't exist

    employee_data = employee_ref.to_dict()

    # Check if the role is 'driver'
    if employee_data.get('role') != 'driver':
        return HttpResponseForbidden(f"{employee_data.get('role')} is not authorized to access this driver page. ")  # Redirect if role is not driver

    return render(request, 'driver_dashboard.html', {'employee': employee_data})

def my_current_booking(request):
    uid = request.session.get('employee_uid')
    if not uid:
        return redirect('driver_login')  # Redirect if employee_uid is not in session

    employee_data = db.collection('employees').document(uid).get().to_dict()
    return render(request, 'my_current_booking.html', {'employee': employee_data})

def driver_profile(request):
    uid = request.session.get('employee_uid')
    if not uid:
        return redirect('driver_login')  # Redirect if employee_uid is not in session

    employee_data = db.collection('employees').document(uid).get().to_dict()
    return render(request, 'driver_profile.html', {'employee': employee_data})





def index(request):
     return render(request, 'index.html')

    


    
# Create bus views here.
def bus_bookings(request):
    uid = request.session.get('employee_uid')
    if not uid:
        return redirect('patner_login') 

    employee_ref = db.collection('employees').document(uid).get()
    if not employee_ref.exists:
        return redirect('patner_login')  # Redirect if employee doesn't exist

    employee_data = employee_ref.to_dict()

    # Check if the role is 'patner'
    if employee_data.get('role') != 'patner':
        return HttpResponseForbidden(f"{employee_data.get('role')} is not authorized to access this patner page. ")  # Redirect if role is not driver


    bookings_ref = db.collection("bus_bookings").stream()
    bookings = []

    for booking in bookings_ref:
        booking_data = booking.to_dict()
        booking_data["id"] = booking.id
        
        user_id = booking_data.get("userId")

        # Fetch user details
        user_ref = db.collection("users").document(user_id).get()
        user_data = user_ref.to_dict() if user_ref.exists else {}

        booking_data["user"] = user_data
        bookings.append(booking_data)

    return render(request, "bus_bookings.html", {"bookings": bookings})

# Create velet views here.
def velet_bookings(request):
    bookings_ref = db.collection("valet_bookings").stream()
    bookings = []

    for booking in bookings_ref:
        booking_data = booking.to_dict()
        booking_data["id"] = booking.id  # FIXED: Add Firestore Document ID
        if booking_data.get("status") == "Pending":
            user_id = booking_data.get("userId")

            # Fetch user details
            user_ref = db.collection("users").document(user_id).get()
            user_data = user_ref.to_dict() if user_ref.exists else {}

            booking_data["user"] = user_data
            bookings.append(booking_data)

    return render(request, "velet_bookings.html", {"bookings": bookings})

def driving_class_bookings(request):
    bookings_ref = db.collection("driving class bookings").stream()
    bookings = []

    for booking in bookings_ref:
        booking_data = booking.to_dict()
        booking_data["id"] = booking.id  # FIXED: Add Firestore Document ID
        if booking_data.get("status") == "Pending":
            user_id = booking_data.get("userId")

            # Fetch user details
            user_ref = db.collection("users").document(user_id).get()
            user_data = user_ref.to_dict() if user_ref.exists else {}

            booking_data["user"] = user_data
            bookings.append(booking_data)

    return render(request, "driving_class_bookings.html", {"bookings": bookings})

def monthly_bookings(request):
    bookings_ref = db.collection("monthly bookings").stream()
    bookings = []

    for booking in bookings_ref:
        booking_data = booking.to_dict()
        booking_data["id"] = booking.id  # FIXED: Add Firestore Document ID
        if booking_data.get("status") == "Pending":
            user_id = booking_data.get("userId")

            # Fetch user details
            user_ref = db.collection("users").document(user_id).get()
            user_data = user_ref.to_dict() if user_ref.exists else {}

            booking_data["user"] = user_data
            bookings.append(booking_data)

    return render(request, "monthly_bookings.html", {"bookings": bookings})

def weakly_bookings(request):
    bookings_ref = db.collection("weakly_bookings").stream()
    bookings = []

    for booking in bookings_ref:
        booking_data = booking.to_dict()
        booking_data["id"] = booking.id  # FIXED: Add Firestore Document ID
        if booking_data.get("status") == "Pending":
            user_id = booking_data.get("userId")

            # Fetch user details
            user_ref = db.collection("users").document(user_id).get()
            user_data = user_ref.to_dict() if user_ref.exists else {}

            booking_data["user"] = user_data
            bookings.append(booking_data)

    return render(request, "weakly_bookings.html", {"bookings": bookings})


def hourly_bookings(request):
    bookings_ref = db.collection("hourly_bookings").stream()
    bookings = []

    for booking in bookings_ref:
        booking_data = booking.to_dict()
        booking_data["id"] = booking.id  # FIXED: Add Firestore Document ID
        if booking_data.get("status") == "Pending":
            user_id = booking_data.get("userId")

            # Fetch user details
            user_ref = db.collection("users").document(user_id).get()
            user_data = user_ref.to_dict() if user_ref.exists else {}

            booking_data["user"] = user_data
            bookings.append(booking_data)

    return render(request, "hourly_bookings.html", {"bookings": bookings})

def my_weakly_bookings(request):
    uid = request.session.get('employee_uid')
    if not uid:
        return redirect('driver_login')

    bookings_ref = db.collection("weakly_bookings").where("accepted_by", "==", uid).stream()
    bookings = []

    for booking in bookings_ref:
        
        booking_data = booking.to_dict()
        booking_data["id"] = booking.id  # FIXED: Add Firestore Document ID
        if booking_data.get("status")  in ["Accepted", "On the Way", "Ongoing"]:
            user_id = booking_data.get("userId")

            # Fetch user details
            user_ref = db.collection("users").document(user_id).get()
            user_data = user_ref.to_dict() if user_ref.exists else {}

            booking_data["user"] = user_data
            bookings.append(booking_data)

    return render(request, "my_weakly_bookings.html", {"bookings": bookings})

def my_hourly_bookings(request):
    uid = request.session.get('employee_uid')
    if not uid:
        return redirect('driver_login')
    bookings_ref = db.collection("hourly_bookings").where("accepted_by", "==", uid).stream()
    bookings = []

    for booking in bookings_ref:
        
        booking_data = booking.to_dict()
        booking_data["id"] = booking.id  # FIXED: Add Firestore Document ID
        if booking_data.get("status")  in ["Accepted", "On the Way", "Ongoing"]:
            user_id = booking_data.get("userId")

            # Fetch user details
            user_ref = db.collection("users").document(user_id).get()
            user_data = user_ref.to_dict() if user_ref.exists else {}

            booking_data["user"] = user_data
            bookings.append(booking_data)

    return render(request, "my_hourly_bookings.html", {"bookings": bookings})


def my_bookings(request):
    # Get the logged-in employee's ID
    uid = request.session.get('employee_uid')
    if not uid:
        return redirect('driver_login')

    collections = [
        
        'driving_class_bookings',
        'valet_bookings',
        'monthly_bookings',
        'weakly_bookings',
        'hourly_bookings'
    ]

    bookings = []

    try:
        for collection in collections:
            bookings_ref = db.collection(collection).where("accepted_by", "==", uid).stream()
            for booking in bookings_ref:
                booking_data = booking.to_dict()
                booking_data["id"] = booking.id  # Firestore Document ID
                booking_data["collection"] = collection  # Collection name
                
                # Fetch user details using userId from "users" collection
                user_id = booking_data.get("userId")
                if user_id:
                    user_doc = db.collection("users").document(user_id).get()
                    if user_doc.exists:
                        booking_data["user_details"] = user_doc.to_dict()
                    else:
                        booking_data["user_details"] = {"Error": "User not found"}
                else:
                    booking_data["user_details"] = {"Error": "User ID missing"}

                bookings.append(booking_data)
    except Exception as e:
        messages.error(request, f"Error fetching bookings: {str(e)}")

    return render(request, 'my_bookings.html', {'bookings': bookings})

@csrf_exempt
def update_booking_amount(request, collection):
    if request.method == 'POST':
        data = json.loads(request.body)
        booking_id = data.get('booking_id')
        added_amount = data.get('added_amount')
        total_amount = data.get('total_amount')
        extra = data.get('extra')

        try:
            db.collection(collection).document(booking_id).update({
                "extra": extra,
                "addedAmount": added_amount,
                "total_amount": total_amount
            })
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
@csrf_exempt
def update_booking_status_gen(request, collection):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            bookingId = data.get("booking_id")
            status = data.get("status")
            cancel_reason = data.get('reason', '')

            if not bookingId:
                return JsonResponse({"success": False, "message": "Missing booking ID"}, status=400)
            
            if not collection:
                return JsonResponse({"success": False, "message": "Missing collection name"}, status=400)

            # Get the logged-in employee's ID from the session
            employee_uid = request.session.get('employee_uid')
            if not employee_uid:
                return JsonResponse({"success": False, "message": "User not logged in"}, status=401)

            # Fetch the booking document
            booking_ref = db.collection(collection).document(bookingId)
            booking_doc = booking_ref.get()

            if not booking_doc.exists:
                return JsonResponse({"success": False, "message": "Booking not found"}, status=404)

            # Update the status and accepted_by fields
            update_data = {"status": status, "accepted_by": employee_uid}

            if status == "Canceled" and cancel_reason:
                update_data['cancel_reason'] = cancel_reason

            booking_ref.update(update_data)

            booking_ref.update(update_data)
            return JsonResponse({"success": True, "message": "Status updated successfully"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def upload_file_to_firebase(file, filename):
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_file(file)
    blob.make_public()
    return blob.public_url





def register_employee(request):
    uid = request.session.get('employee_uid')
    if not uid:
        return redirect('admin_login')

    employee_ref = db.collection('employees').document(uid).get()
    if not employee_ref.exists:
        return redirect('patner_login')  # Redirect if employee doesn't exist

    employee_data = employee_ref.to_dict()

    # Check if the role is 'patner'
    if employee_data.get('role') != 'admin':
        return HttpResponseForbidden(f"{employee_data.get('role')} is not authorized to access this admin page. ") 
    if request.method == "POST":
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            try:
                # Create Firebase Authentication User
                user = auth.create_user(email=data['email'], password=data['password'])
                uid = user.uid  # Employee ID will be the same as UID
                logging.info(f"User created successfully with UID: {uid}")

                # Upload files to Firebase Storage safely
                profile_pic_url = upload_file_to_firebase(request.FILES.get('profile_pic'), f"{uid}_profile.jpg") if request.FILES.get('profile_pic') else None
                resume_url = upload_file_to_firebase(request.FILES.get('resume'), f"{uid}_resume.pdf") if request.FILES.get('resume') else None
                dl_url = upload_file_to_firebase(request.FILES.get('dl'), f"{uid}_dl.jpg") if request.FILES.get('dl') else None

                # Store Employee Data in Firestore
                employee_data = {
                    'employee_id': uid,  # Employee ID same as UID
                    'name': data['name'],
                    'address': data['address'],
                    'phone': data['phone'],
                    'email': data['email'],
                    'role': data['role'],
                    'profile_pic': profile_pic_url,
                    'resume': resume_url,
                    'dl': dl_url
                }

                db.collection('employees').document(uid).set(employee_data)
                logging.info(f"Employee data stored successfully in Firestore for UID: {uid}")

                # Show success message
                messages.success(request, "Employee registered successfully!")

                # Redirect to a success page with a new registration option
                return render(request, 'register_success.html', {'employee_id': uid})

            except Exception as e:
                logging.error(f"Error registering employee: {str(e)}")
                messages.error(request, f"Error: {str(e)}")

    else:
        form = EmployeeRegistrationForm()

    return render(request, 'register_employee.html', {'form': form})

def driver_login(request):
    if request.session.get('employee_uid'):
        return redirect('driver_dashboard')
      # Redirect if already logged in

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = auth.get_user_by_email(email)
            uid = user.uid
            
            # Retrieve role from Firestore
            employee_data = db.collection('employees').document(uid).get().to_dict()
            if not employee_data:
                messages.error(request, "Unauthorized user.")
                return redirect('driver_login')

            role = employee_data.get('role')

            if role != "driver":
                messages.error(request, "Access Denied: Only drivers can log in.")
                return redirect('driver_login')
            
            # Store session data
            request.session['employee_uid'] = uid
            request.session['role'] = role

            return redirect('driver_dashboard')
        
        except Exception as e:
            messages.error(request, f"Login Failed: {str(e)}")

    return render(request, 'driver_login.html')

def patner_login(request):
    if request.session.get('employee_uid'):
        return redirect('bus_bookings')
      # Redirect if already logged in

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = auth.get_user_by_email(email)
            uid = user.uid
            
            # Retrieve role from Firestore
            employee_data = db.collection('employees').document(uid).get().to_dict()
            if not employee_data:
                messages.error(request, "Unauthorized user.")
                return redirect('patner_login')

            role = employee_data.get('role')

            if role != "patner":
                messages.error(request, "Access Denied: Only patner can log in.")
                return redirect('patner_login')
            
            # Store session data
            request.session['employee_uid'] = uid
            request.session['role'] = role

            return redirect('bus_bookings')
        
        except Exception as e:
            messages.error(request, f"Login Failed: {str(e)}")

    return render(request, 'patner_login.html')

def admin_login(request):
    if request.session.get('employee_uid'):
        return redirect('register_employee')
      # Redirect if already logged in

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = auth.get_user_by_email(email)
            uid = user.uid
            
            # Retrieve role from Firestore
            employee_data = db.collection('employees').document(uid).get().to_dict()
            if not employee_data:
                messages.error(request, "Unauthorized user.")
                return redirect('admin_login')

            role = employee_data.get('role')

            if role != "admin":
                messages.error(request, "Access Denied: Only admin can log in.")
                return redirect('admin_login')
            
            # Store session data
            request.session['employee_uid'] = uid
            request.session['role'] = role

            return redirect('admin_dashboard')
        
        except Exception as e:
            messages.error(request, f"Login Failed: {str(e)}")

    return render(request, 'admin_login.html')




def employee_logout(request):
    request.session.flush()  # Clear session data
    messages.success(request, "Logged out successfully.")
    return redirect('index')


def admin_dashboard(request):
    uid = request.session.get('employee_uid')
    if not uid:
        return redirect('admin_login')

    employee_ref = db.collection('employees').document(uid).get()
    if not employee_ref.exists:
        return redirect('patner_login')  # Redirect if employee doesn't exist

    employee_data = employee_ref.to_dict()

    # Check if the role is 'patner'
    if employee_data.get('role') != 'admin':
        return HttpResponseForbidden(f"{employee_data.get('role')} is not authorized to access this admin page. ") 

    return render(request, 'admin_dashboard.html')