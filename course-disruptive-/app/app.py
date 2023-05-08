from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from langdetect import detect

import spacy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+'root'+':'+'123'+'@'+'127.0.0.1:3306'+'/'+'courses'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


app.config['DEBUG'] = True


class courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50))
    course_price = db.Column(db.Numeric(6,2))
    course_description = db.Column(db.String(200))
    course_rating = db.Column(db.Numeric(3,1))
    course_reviews_count = db.Column(db.Integer)

    def __init__(self, course_name, course_price, course_description, course_rating, course_reviews_count):
        self.course_name = course_name
        self.course_price = course_price
        self.course_description = course_description
        self.course_rating = course_rating
        self.course_reviews_count = course_review

class cursos(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50))
    course_price = db.Column(db.Numeric(6,2))
    course_description = db.Column(db.String(200))
    course_rating = db.Column(db.Numeric(3,1))
    course_reviews_count = db.Column(db.Integer)

    def __init__(self, course_name, course_price, course_description, course_rating, course_reviews_count):
        self.course_name = course_name
        self.course_price = course_price
        self.course_description = course_description
        self.course_rating = course_rating
        self.course_reviews_count = course_reviews_count
 

class cursosPalabrasClave(db.Model):
    __tablename__ = 'cursos_keyword'
    course_id = db.Column(db.Integer, db.ForeignKey('cursos.course_id'), primary_key=True)
    keyword = db.Column(db.String(50), primary_key=True)

    def __init__(self, course_id, keyword):
        self.course_id = course_id
        self.keyword = keyword


class CourseKeyword(db.Model):
    __tablename__ = 'course_keyword'
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), primary_key=True)
    keyword = db.Column(db.String(50), primary_key=True)

    def __init__(self, course_id, keyword):
        self.course_id = course_id
        self.keyword = keyword



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        curso = request.form['curso']
        table_names = {
            'es_core_news_sm': 'cursosPalabrasClave',
            'en_core_web_sm': 'CourseKeyword'
        }

        


        if curso.lang_ == 'en':
            print("en")
            lang_model = 'en_core_web_sm'
        else:
            print("es")
            lang_model = 'es_core_news_sm'

        
        npl = spacy.load(lang_model)
        doc = npl(curso)

        
        keywords = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
        num_keywords = len(keywords)

        table_name = table_names[lang_model]
        

        #results = cursosPalabrasClave.query.filter(cursosPalabrasClave.keyword.in_(keywords)).all()
        results = CourseKeyword.query.filter(CourseKeyword.keyword.in_(keywords)).all()

        courses = {}
        for result in results:
            if result.course_id not in courses:
                courses[result.course_id] = [result.keyword]
            else:
                courses[result.course_id].append(result.keyword)
        matching_courses = []
        for course_id, keywords in courses.items():
            if len(keywords) == num_keywords:
                course = cursos.query.get(course_id)
                course_dict = {
                    'course_id': course.course_id,
                    'course_name': course.course_name,
                    'course_price': course.course_price,
                    'course_description': course.course_description,
                    'course_rating': course.course_rating,
                    'course_reviews_count': course.course_reviews_count,
                    'keyword': keywords
                }
                matching_courses.append(course_dict)
        
        print(matching_courses)
        
        
        return f'El nombre del curso es: <br><br> {matching_courses}'



    else:
        return render_template('index.html')    
        


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(port=5000, debug=True)