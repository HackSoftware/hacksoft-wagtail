USERNAME="$1"

echo "Using pg user: $USERNAME"

echo "Fetching latest dump ...\n"
curl -o db.dump `heroku pg:backups public-url --app hacksoft-website-staging`

echo "Recreating database ...\n"
dropdb --if-exists hacksoft
sudo -u postgres createdb -O $USERNAME hacksoft

echo "Starting pg_restore ...\n"
pg_restore -U $USERNAME -d hacksoft -c -j 4 db.dump
rm db.dump

echo "Migrations and data ...\n"
python manage.py migrate
