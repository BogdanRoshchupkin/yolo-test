IMAGE_NAME = yolo-car-service
CONTAINER_NAME = yolo_car_service
PORT ?= 8000
DEVICE ?= mps
IP ?= 0.0.0.0

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm -p $(PORT):$(PORT) -e DEVICE=$(DEVICE) -e IP=$(IP) -e PORT=$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)
