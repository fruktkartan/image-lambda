run_tests:
	python3 -m flake8;
	python3 -m pytest test/*

publish:
	pip3 install --target ./packages -r requirements/prod.txt --upgrade;
	rm -f fk_images.zip; \
	cd packages; \
	zip -r9 ../fk_images.zip .; \
	cd ..; \
	zip -g fk_images.zip handler.py; \
	aws s3 cp ./ s3://fk-lambda-repo/ --recursive --exclude "*" --include "*.zip"; \
	aws lambda update-function-code --function-name fruktkartan-image --region eu-north-1 --s3-bucket fk-lambda-repo --s3-key fk_images.zip
