SHELL_FOLDER=$(dirname $(readlink -f "$0"))
cd $SHELL_FOLDER
git add rss.db
git commit -m"backup database"
git pull --no-edit
git push origin master
