echo "BUILD START"
Python3.11.4 -m pip install -r requirements.txt
Python3.11.4 manage.py collectstatic --noinput --clear
echo "BUILD END"