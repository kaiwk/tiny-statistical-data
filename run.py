from website import register_blueprint

app = register_blueprint()

if __name__ == '__main__':
    app.run(debug=True)
