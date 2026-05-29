for i in {1..50}; do
  curl localhost:8000/api/catalogue/hostname &
done