#! /usr/bin/python
from __future__ import division
from math import floor
import sys
from os import listdir
import os.path
from PIL import Image

def testEqual(expected, actual):
	if  actual == expected:
		print "Test PASSED"
	else:
		print "Test FAILED! Expected %s, got %s" % (expected, actual)

def TestCalculateFunction():
	testEqual(calculatePaddedDimensions( (10, 10), (3, 2) ), (15, 10) )
	testEqual(calculatePaddedDimensions( (10, 20), (3, 2) ), (13, 20) )
	testEqual(calculatePaddedDimensions( (40, 30), (3, 2) ), (45, 30) )
	testEqual(calculatePaddedDimensions( (30, 20), (8, 10) ), (30, 24) )
	testEqual(calculatePaddedDimensions( (1, 4), (5, 1) ), (1, 5) )

def calculatePaddedDimensions(startingSize, targetAspectRatio):
	normalizedStartingAspect = (startingSize[0] / min(startingSize), startingSize[1] / min(startingSize))
	normalizedTargetAspect = (targetAspectRatio[0] / min(targetAspectRatio), targetAspectRatio[1] / min(targetAspectRatio))

	scalingFactor = max(normalizedTargetAspect) / min(normalizedTargetAspect)
	inverseScalingFactor = 1 / scalingFactor

	longEdgeIndex = startingSize.index(max(startingSize))
	shortEdgeIndex = startingSize.index(min(startingSize))

	# decide whether to pad short edge or long edge
	if (max(normalizedStartingAspect) / min(normalizedStartingAspect)) < scalingFactor:
		#need to pad long edge (e.g. 4:3 into 4x6)
		shortPixels = startingSize[shortEdgeIndex]
		if longEdgeIndex == 0:
			targetSize = (shortPixels * scalingFactor, shortPixels)
		else:
			targetSize = (shortPixels, shortPixels * scalingFactor)
	else:
		#need to pad short edge (e.g. panorama into 4x6, 3:2 into 8x10)
		longPixels = startingSize[longEdgeIndex]
		if shortEdgeIndex == 0:
			targetSize = (longPixels * inverseScalingFactor, longPixels)
		else:
			targetSize = (longPixels, longPixels * inverseScalingFactor)

	targetSize = (int(targetSize[0]), int(targetSize[1]))
	return targetSize

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print 'usage: pad_image_to_aspect.py <source_dir> <aspect_w> <aspect_h>'
		sys.exit(2)
	source_dir = sys.argv[1]
	output_dir = source_dir + "/PaddedImages"
	if not os.path.isdir(output_dir):
		os.mkdir(output_dir)


	accepted_formats = ["jpg", "jpeg", "JPG", "JPEG"]
	image_files = [str(f) for f in listdir(source_dir) if f.split(".")[-1] in accepted_formats]
	for image in image_files:
		filename = image.split(".")[0]
		start_image = Image.open(os.path.join(source_dir, image))
		# print "Starting size is %s" % (start_image.size,)
		# print "New size is %s \n" % (calculatePaddedDimensions(start_image.size, (3, 2)),)
		start_size = start_image.size
		padded_size = calculatePaddedDimensions(start_size, (3, 2))
		padded_image = Image.new("RGB", padded_size, color = (255, 255, 255))
		padded_image.paste(start_image, ((padded_size[0]-start_size[0])//2,
	                      (padded_size[1]-start_size[1])//2))
		padded_image.save(os.path.join(output_dir, filename + ".padded.jpg"))

