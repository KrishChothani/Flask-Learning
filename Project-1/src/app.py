# from flask import Flask , redirect, url_for

# app = Flask(__name__)

# @app.route('/')
# def welcome():
#     return "<h1>Welcome to hey krish</h1>"


# @app.route('/member')
# def member():
#     return "<h1>Welcome to hey member</h1>"

# @app.route('/success/<int:score>')
# def success(score):
#     return "<h1>Pass and success score is </h1>" + str(score)


# @app.route('/fail/<int:score>')
# def fail(score):
#     return "<h1>Fail and fail score is </h1>" + str(score)

# @app.route('/results/<int:marks>')
# def results(marks):
#     result=""
#     if marks <50:
#         result = "fail"
#     else :
#         result = "success"
#     return redirect(url_for(result , score=marks))
        




# if __name__ == '__main__':
#     app.run(debug=True , port =2590)