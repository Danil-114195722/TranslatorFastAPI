# basedir for all project
basedir=$(dirname "$(realpath "$0")")

# prod/dev arg
mode=$1

if [ "$mode" == "prod" ]; then
  python3 "$basedir/create_tables.py"
  uvicorn main:app --host 0.0.0.0 --port 8001
else
  if [ "$mode" == "dev" ]; then
    python3 "$basedir/create_tables.py"
    uvicorn main:app --reload
  else
    echo 'Use "dev" arg to start app in DEVELOPMENT mode.'
    echo 'Or use "prod" arg to start app in PRODUCTION mode'
  fi
fi
