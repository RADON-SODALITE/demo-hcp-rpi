prepare:
	rm -f radon && \
	ln -sf ../ThumbnailGeneration_RPi radon

deploy: prepare
	opera deploy -i input.yaml test.yaml