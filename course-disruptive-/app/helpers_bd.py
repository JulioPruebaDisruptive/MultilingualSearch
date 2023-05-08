from app import db, courses, cursos

    data = courses.query.all()

        results = []
        results_sorted = []


        unique_results = set()
        for row in data:
            new_result = {
                "course_id": row.course_id,
                "course_name": row.course_name,
                "course_price": float(row.course_price),
                "course_description": row.course_description,
                "course_rating": float(row.course_rating),
                "course_reviews_count": row.course_reviews_count
            }
            unique_results.add(tuple(new_result.items()))

        unique_results = set()
        for row in data:
            new_result = {
                "course_id": row.course_id,
                "course_name": row.course_name,
                "course_price": float(row.course_price),
                "course_description": row.course_description,
                "course_rating": float(row.course_rating),
                "course_reviews_count": row.course_reviews_count
            }
            unique_results.add(tuple(new_result.items()))



        results = [dict(item) for item in unique_results]
        results_sorted = sorted(results, key=lambda k: k['course_id'])


        print("--")
        print("--")
        print(len(results_sorted))
        print("--")
        print("--")
        print("--")
        for row in results_sorted:
            print(row)






        

        nlp = spacy.load("en_core_web_sm")

        keywords_by_course = {}

        for course in results_sorted:
            keywords = set()
            text = ' '.join(str(value) for value in course.values())
            doc = nlp(text)
            for token in doc:
                if token.is_stop or token.is_punct or token.is_space:
                    continue
                if token.lemma_.lower() not in keywords:
                    keywords.add(token.lemma_.lower())
            keywords_by_course[course['course_id']] = keywords

        print("--")
        print(type(keywords_by_course))
        print(len(keywords_by_course))
        print("--")
        print("--")
        print("--")

        for course_id, keywords in keywords_by_course.items():
            print(f"course_id: {course_id}, key_words: {keywords}")





        for course_id, keyword in keywords_by_course.items():
            for keyword in keywords:
                course_keyword = CourseKeyword(course_id=course_id, keyword=keyword)
                db.session.add(course_keyword)
        
        db.session.commit()

