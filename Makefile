

all: people network


network:
		python3 generate_js.py


people:
		python3 process_csv.py family_fixed.csv
