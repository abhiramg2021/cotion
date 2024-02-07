# Cotion

This is a Canvas to Notion bridge. It allows you to update your Notion database with the list of assignments from Canvas. This code is written so that it be run every day to update the Notion database with the latest assignments.

## Configuration

I have attached a `config.template.json` file to the repo, use that as a template to create your own `config.json` file.

### Canvas

#### Domain

For the `DOMAIN` field, you should put the domain of your Canvas instance. For example, if your Canvas instance is `https://canvas.instructure.com`, then you should put `canvas.instructure.com` in the `DOMAIN` field.

#### Token

For the `TOKEN` field, you should generate a Canvas API token. You can do this by going to your Canvas profile settings and generating a new access token, then pasting that token into the `TOKEN` field.

### Notion

#### Token

For the `TOKEN` field, you should generate a Notion API token. You can do this by going to the Notion integrations page and creating a new Personal integration called `cotion`. Then, you can paste the token into the `TOKEN` field.

In your Notion database, add a connection for the `cotion` integration. Then, cotion should have the ability to see your database.

#### Database ID

For the `DATABASE_ID` field, you should put the ID of the Notion database that you want to update. You can get this by going to the Notion database and copying the URL. The ID is the part of the url before the `?` character.

#### Database Properties

Remember, this database should have the following properties:

- Title : (Name)
- Due : (Date)
- Topic : (Select)

## Installation & Running the code

1. Clone the repo
2. Run `pip install -r requirements.txt`
3. Create a `config.json` file using the `config.template.json` file as a template
4. Run `python main.py`

## Command Line Flags

- `--force` If this flag is specified, the script will run even though it was already run today.
- `--computer` I specified this flag so that I can run the script on my computer as a startup process on my terminal. This flag suppresses some print warnings that would be annoying otherwise everytime that I opened a new terminal.
