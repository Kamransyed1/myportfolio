from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
from functools import wraps
from io import BytesIO
from werkzeug.exceptions import HTTPException, NotFound

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_entries.db'
app.config['UPLOAD_FOLDER'] = r'C:\Users\ABC\OneDrive\Desktop\myportfolio\uploads_folder'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.secret_key = 'your_secure_random_key'


# Initial admin credentials
admin_username = "admin"
admin_password = "Kamransaeed@141001"

#contact page form submission entries model
class FormEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)

#home page skills animation moderl 
class HomePage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name1 = db.Column(db.String(100))
    name2 = db.Column(db.String(100))
    name3 = db.Column(db.String(100))

#home page introduction text model
class HomePageIntroduction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strong = db.Column(db.String(100))
    line1 = db.Column(db.String(100))
    line2 = db.Column(db.String(100))
    line3 = db.Column(db.String(100))

#contact page details model 
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    freelance_available = db.Column(db.String(10), nullable=False)


#resume_intro page model for intro text
class ResumeIntro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intro_text = db.Column(db.Text, nullable=False)


#resume_intro page details model
class ResumeInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.String(10), nullable=False)
    residence = db.Column(db.String(100), nullable=False)
    freelance = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)

#resume_intro page services model
class ServiceInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    svg_filename = db.Column(db.String(255), nullable=True)  # Store the file name in the database
    svg_content = db.Column(db.Text, nullable=False)  # Store the SVG content in the database
    service_name = db.Column(db.String(100), nullable=False)
    service_description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"ServiceInfo(id={self.id}, service_name={self.service_name})"

    def save_svg_file(self, file):
        # Save the uploaded SVG file to the server and update the model
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            self.svg_filename = filename
            with open(file_path, 'r') as svg_file:
                self.svg_content = svg_file.read()

#resume_page coding skills model
class CodingSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(50), nullable=False)
    percentage = db.Column(db.Integer, nullable=False)

#resume_page knowledge model
class Knowledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    knowledge_name = db.Column(db.String(50), nullable=False)

#resume_page team model
class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(50), nullable=False)
    designation = db.Column(db.String(50), nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    image_content = db.Column(db.Text, nullable=True)  # Store the image content in the database

    def __repr__(self):
        return f"TeamMember(id={self.id}, member_name={self.member_name})"

    def save_image_file(self, file):
        # Save the uploaded image file to the server and update the model
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            self.image_filename = filename
            with open(file_path, 'rb') as image_file:
                self.image_content = image_file.read()
    
#resume_page testimonial model
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(50), nullable=False)
    client_designation = db.Column(db.String(50), nullable=False)
    client_reviews = db.Column(db.Text, nullable=True)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(100), nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    post_image = db.Column(db.LargeBinary, nullable=True)

    def __repr__(self):
        return f"Post(title={self.post_title}, content={self.post_content}, image={self.post_image})"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Move db.create_all() inside the app context
with app.app_context():
    db.create_all()



# Define the login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@login_required
def admin():
    return render_template('admin/index.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    global admin_password
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == admin_username and password == admin_password:
            # Successful login, set session variable and redirect to admin dashboard
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            # Incorrect credentials, render login page with an error message
            return render_template('admin/login.html', error='Invalid username or password')

    return render_template('admin/login.html', error=None)


# Change password route
# Change password route
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    global admin_password  # Move the global declaration here
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Check if the old password matches the current password
        if old_password == admin_password:
            # Check if the new password and confirm password match
            if new_password == confirm_password:
                # Update the admin password
                admin_password = new_password
                return redirect(url_for('admin'))
            else:
                return render_template('admin/change_password.html', error='New password and confirm password do not match')
        else:
            return render_template('admin/change_password.html', error='Incorrect old password')

    return render_template('admin/change_password.html', error=None)


# Logout route
@app.route('/logout')
def logout():
    # Clear the session variable to log out the user
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/contact_q', methods=['GET', 'POST'])
@login_required
def contact_q():
    if request.method == 'POST':
        phone = request.form['phone']
        email = request.form['email1']
        address = request.form['address']
        freelance_available = request.form['freelanceavailable']

        new_entry = Contact(phone=phone, email=email, address=address, freelance_available=freelance_available)
        db.session.add(new_entry)
        db.session.commit()

        # Redirect to avoid form resubmission
        return redirect(url_for('contact_q'))

    entries = FormEntry.query.all()
    entries_form = Contact.query.all()
    return render_template('admin/contact_q.html', entries=entries, entries_form=entries_form)



@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['postTitle']
        content = request.form['postContent']
        
        # Check if the post image file is part of the request
        if 'postImage' not in request.files:
            return "No file part"

        post_image = request.files['postImage']

        # Check if the file is allowed and has a filename
        if post_image.filename == '' or not allowed_file(post_image.filename):
            return "Invalid file"

        # Read the image data and store it in the database
        image_data = post_image.read()

        # Create a new Post instance and add it to the database
        new_post = Post(post_title=title, post_content=content, post_image=image_data)
        db.session.add(new_post)
        
        try:
            db.session.commit()
            return redirect(url_for('add_post'))
        except Exception as e:
            # Print the error for debugging
            print(f"Error: {e}")
            return "Error saving to the database"
    
    # Retrieve all posts from the database
    posts = Post.query.all()
    return render_template('admin/add_post.html', posts=posts)

@app.route('/image/<int:post_id>')
def image(post_id):
    post = Post.query.get_or_404(post_id)
    return send_file(BytesIO(post.post_image), mimetype='image/jpeg')


@app.route('/post-details/<int:post_id>')
@login_required
def post_details(post_id):
    post = Post.query.get(post_id)

    if post is None:
        raise NotFound("Post not found")

    return render_template('post_details.html', post=post)













@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    entries_home = HomePage.query.all()
    entries_introduction = HomePageIntroduction.query.all()

    if request.method == 'POST':
        form_type = request.form['form_type']

        if form_type == 'home':
            name1 = request.form['name1']
            name2 = request.form['name2']
            name3 = request.form['name3']

            form_entry = HomePage(name1=name1, name2=name2, name3=name3)
            db.session.add(form_entry)
        elif form_type == 'introduction':
            strong = request.form['strong']
            line1 = request.form['line1']
            line2 = request.form['line2']
            line3 = request.form['line3']

            form_entry = HomePageIntroduction(strong=strong, line1=line1, line2=line2, line3=line3)
            db.session.add(form_entry)

        db.session.commit()

        # Redirect to avoid form resubmission
        return redirect(url_for('home'))

    return render_template('admin/home.html', entries_home=entries_home, entries_introduction=entries_introduction)



@app.route('/resume_intro', methods=['GET', 'POST'])
@login_required
def resume_intro():
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'intro':
            intro_text = request.form.get('resume_intro_text')
            new_intro = ResumeIntro(intro_text=intro_text)
            db.session.add(new_intro)

        elif form_type == 'info':
            age = request.form.get('age')
            residence = request.form.get('residence')
            freelance = request.form.get('freelance')
            address = request.form.get('address')
            phone = request.form.get('phone')
            email = request.form.get('email')

            new_info = ResumeInfo(age=age, residence=residence, freelance=freelance, address=address, phone=phone, email=email)
            db.session.add(new_info)

        db.session.commit()
        # Redirect to avoid form resubmission
        return redirect(url_for('resume_intro'))

    entries_intro = ResumeIntro.query.all()
    entries_info = ResumeInfo.query.all()

    return render_template('admin/resume_intro.html', entries_intro=entries_intro, entries_info=entries_info)


@app.route('/resume_services', methods=['GET', 'POST'])
@login_required
def resume_services():
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'service':
            svg_file = request.files.get('svg_file')
            service_name = request.form.get('service_name')
            service_description = request.form.get('service_description')

            new_service = ServiceInfo(service_name=service_name, service_description=service_description)
            new_service.save_svg_file(svg_file)

            db.session.add(new_service)
            db.session.commit()

            # Redirect to avoid form resubmission
            return redirect(url_for('resume_services'))

    # Your existing code to display the form or other content
    entries = ServiceInfo.query.all()
    return render_template('admin/resume_services.html', entries=entries)


@app.route('/coding_skills', methods=['GET', 'POST'])
@login_required
def coding_skills():
    if request.method == 'POST':
        # Get form data
        skill_name = request.form['skill_name']
        percentage = int(request.form['percentage'])

        # Create a new CodingSkill instance
        new_skill = CodingSkill(skill_name=skill_name, percentage=percentage)

        # Add the new skill to the database
        db.session.add(new_skill)
        db.session.commit()

        # Redirect to the same page after submitting the form
        return redirect(url_for('coding_skills'))

    # If it's a GET request, render the template
    skills = CodingSkill.query.all()
    return render_template('admin/coding_skills.html', skills=skills)

@app.route('/resume_knowledge', methods=['GET', 'POST'])
@login_required
def resume_knowledge():
    if request.method == 'POST':
        # Get form data
        knowledge_name = request.form['knowledge_name']

        # Create a new Knowledge instance
        new_knowledge = Knowledge(knowledge_name=knowledge_name)

        # Add the new knowledge to the database
        db.session.add(new_knowledge)
        db.session.commit()

        # Redirect to the same page after submitting the form
        return redirect(url_for('resume_knowledge'))

    # If it's a GET request, render the template
    knowledge_data = Knowledge.query.all()
    return render_template('admin/resume_knowledge.html', knowledge_data=knowledge_data)

@app.route('/resume_team', methods=['GET', 'POST'])
@login_required
def resume_team():
    if request.method == 'POST':
        # Extract form data
        member_name = request.form.get('member_name')
        designation = request.form.get('designation')
        image_file = request.files.get('image')

        # Create a new TeamMember instance
        new_team_member = TeamMember(member_name=member_name, designation=designation)

        # Save the image file to the server and update the model
        new_team_member.save_image_file(image_file)

        # Save the TeamMember instance to the database
        db.session.add(new_team_member)
        db.session.commit()

        # Redirect to the same page after submitting the form
        return redirect(url_for('resume_team')) 

    # If it's a GET request, render the template
    team_members = TeamMember.query.all()
    return render_template('admin/resume_team.html', team_members=team_members)


@app.route('/resume_testimonials', methods=['GET', 'POST'])
@login_required
def resume_testimonials():
    if request.method == 'POST':
        # Get form data
        form_type = request.form.get('form_type')

        # Check the form type
        if form_type == 'client':
            client_name = request.form.get('client_name')
            client_designation = request.form.get('client_designation')
            client_reviews = request.form.get('client_reviews')

            # Create a new Client instance and add it to the database
            new_client = Client(client_name=client_name, client_designation=client_designation, client_reviews=client_reviews)
            db.session.add(new_client)
            db.session.commit()

            return redirect(url_for('resume_testimonials'))  # Redirect to the same page after submission

    clients = Client.query.all()
    return render_template('admin/resume_testimonials.html', clients=clients)





@app.route('/')
def index():
    entries_home = HomePage.query.all()
    entries_form = Contact.query.all()
    entries_introduction = HomePageIntroduction.query.all()
    return render_template('index_personal.html', entries_home=entries_home, entries_introduction=entries_introduction, entries_form=entries_form)

@app.route('/resume')
def resume():
    entries_form = Contact.query.all()
    entries = ResumeIntro.query.all()
    entries_info = ResumeInfo.query.all()
    entries = ServiceInfo.query.all()
    skills = CodingSkill.query.all()
    knowledge_data = Knowledge.query.all()
    clients = Client.query.all()
    return render_template('resume_creative.html', entries_form=entries_form, entries=entries, entries_info=entries_info, skills=skills, knowledge_data=knowledge_data, clients=clients) 

@app.route('/work')
def work():
    entries_form = Contact.query.all()
    return render_template('works_creative.html', entries_form=entries_form)

@app.route('/blog')
def blog():
    posts = Post.query.all()
    return render_template('blog.html', posts=posts)

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        form_entry = FormEntry(name=name, email=email, message=message)
        db.session.add(form_entry)
        db.session.commit()

        return redirect(url_for('contacts'))
    entries_form = Contact.query.all()
    entries = FormEntry.query.all()
    return render_template('contacts_creative.html', entries_form=entries_form, entries=entries)

@app.route('/success')
def success():
    return render_template('contacts_creative.html')


@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = FormEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('contact_q'))

@app.route('/delete_contact/<int:entry_id>', methods=['POST'])
def delete_contact(entry_id):
    entry = Contact.query.get(entry_id)

    if entry:
        db.session.delete(entry)
        db.session.commit()

    # Redirect to the page after deletion
    return redirect(url_for('contact_q'))


@app.route('/home/delete/<int:entry_id>', methods=['GET', 'POST'])
def delete_entry_by_id(entry_id):
    # Try to find the entry in HomePageIntroduction
    entry = HomePageIntroduction.query.get(entry_id)

    # If not found, try to find the entry in HomePage
    if not entry:
        entry = HomePage.query.get(entry_id)

    if entry:
        db.session.delete(entry)
        db.session.commit()

    # Redirect to the home page after deletion
    return redirect(url_for('home'))


@app.route('/delete_resume_intro/<int:entry_id>', methods=['POST'])
def delete_resume_intro(entry_id):
    entry = ResumeIntro.query.get_or_404(entry_id)
    
    # Delete the entry
    db.session.delete(entry)
    db.session.commit()

    # Redirect back to the resume_intro route
    return redirect(url_for('resume_intro'))

@app.route('/delete_resume_intfo/<int:entry_id>', methods=['POST'])
def delete_resume_info(entry_id):
    entry = ResumeInfo.query.get_or_404(entry_id)
    
    # Delete the entry
    db.session.delete(entry)
    db.session.commit()

    # Redirect back to the resume_intro route
    return redirect(url_for('resume_intro'))


@app.route('/delete_resume_services/<int:entry_id>', methods=['POST'])
def delete_resume_services(entry_id):
    entry = ServiceInfo.query.get_or_404(entry_id)
    
    # Delete the entry
    db.session.delete(entry)
    db.session.commit()

    # Redirect back to the resume_intro route
    return redirect(url_for('resume_services'))


@app.route('/delete_skill/<int:id>', methods=['POST', 'DELETE'])
def delete_skill(id):
    # Find the skill by ID
    skill = CodingSkill.query.get_or_404(id)

    # Delete the skill from the database
    db.session.delete(skill)
    db.session.commit()

    # Redirect back to the coding_skills page
    return redirect(url_for('coding_skills'))


@app.route('/delete_knowledge/<int:knowledge_id>', methods=['POST'])
def delete_knowledge(knowledge_id):
    knowledge = Knowledge.query.get_or_404(knowledge_id)
    
    db.session.delete(knowledge)
    db.session.commit()
    
    return redirect(url_for('resume_knowledge'))


@app.route('/delete_client/<int:client_id>', methods=['POST', 'DELETE'])
def delete_client(client_id):
    if request.method in ['POST', 'DELETE']:
        client = Client.query.get(client_id)
        if client:
            db.session.delete(client)
            db.session.commit()

    return redirect(url_for('resume_testimonials'))

@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('add_post'))




if __name__ == '__main__':
    app.run(debug=True)
