from behavior_analysis import init_app

app = init_app()

if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=False, use_reloader=False)
    app.run(host='0.0.0.0', debug=True)
