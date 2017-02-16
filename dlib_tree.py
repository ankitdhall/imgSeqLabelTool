import cv2
import os
import numpy as np
import to_xml
import dlib

class annotate():
	def __init__(self, path, annotation_path, extension, start_from):
		print "initializing..."

		# ignore unintentional clicks and very small boxes with area < threshold
		self.threshold = 1000

		self.path = path
		self.annotation_path = annotation_path
		self.extension = extension

		self.img = None
		self.unedited_img = None
		self.height = -1
		self.width = -1
		self.start_from = start_from

		# store bounding box co-ordinates for a particular image
		self.bbox = []
		
		# whether to use the tracker on a particular image
		self.tracker_flag = False

		# variables for creating rectangles on the image
		self.selection = None
		self.drag_start = None
		self.track_window = None

		# store dlib tracker objects for each bbox
		self.trackers= []

		self.window_name = None

	def render_rectangles(self):
		"""
			renders bbox as rectangles
		"""
		print "render rects"
		for rect in self.bbox:
			xmin, ymin, xmax, ymax = self.keep_coords_in_frame(rect)
			cv2.rectangle(self.img, (xmin, ymin), (xmax, ymax), (255,0,0), 2)
			print "Rendering rectangle...", self.bbox
			cv2.imshow(self.window_name, self.img)
		cv2.imshow(self.window_name, self.img)

	def keep_coords_in_frame(self, rect):
		"""
			ensures that any bbox that exceed the image size are invalid
			clamps invalid co-ordinates
		"""
		xmin, ymin, xmax, ymax = rect
		if xmax > self.width:
			xmax = self.width
		if xmin > self.width:
			xmin = self.width
		if ymax > self.height:
			ymax = self.height
		if ymin > self.height:
			ymin = self.height

		coord = [xmin, ymin, xmax, ymax]
		for i in xrange(4):
			if coord[i] < 0:
				coord[i] = 0
		print "inside keep coords:", coord
		return coord

	def tracker_setup(self):
		"""
			function that creates a list of dlib_tracker objects per bbox
		"""
		print "tracker setup..."
		self.trackers = [dlib.correlation_tracker() for i in range(len(self.bbox))]
		i = 0
		for rect in self.bbox:
			xmin, ymin, xmax, ymax = self.keep_coords_in_frame(rect)
			self.trackers[i].start_track(self.img, dlib.rectangle(xmin, ymin, xmax, ymax))
			i = i + 1

	def on_mouse(self, event, x, y, flags, param):
		"""
			defining mouse behaviour
		"""
		if self.tracker_flag == True:
			return

		if event == cv2.EVENT_LBUTTONDOWN:
			self.drag_start = (x, y)
			self.track_window = None

		if self.drag_start:
			xmin = min(x, self.drag_start[0])
			ymin = min(y, self.drag_start[1])
			xmax = max(x, self.drag_start[0])
			ymax = max(y, self.drag_start[1])
			xmin, ymin, xmax, ymax = self.keep_coords_in_frame([xmin, ymin, xmax, ymax])
			self.selection = (xmin, ymin, xmax, ymax)
			x = self.img.copy()
			cv2.rectangle(x, (xmin, ymin), (xmax, ymax), (255,0,0), 2)
			cv2.imshow(self.window_name, x)
			#self.render_rectangles()

		if event == cv2.EVENT_LBUTTONUP:
			self.drag_start = None
			xmin, ymin, xmax, ymax = self.keep_coords_in_frame([xmin, ymin, xmax, ymax])
			self.track_window = (xmin, ymin, xmax - xmin, ymax - ymin)

			area = (xmax-xmin)*(ymax-ymin)
			if area > self.threshold:
				self.bbox.append(self.selection)
			self.render_rectangles()

	def find_box(self, tracker):
		"""
			retrieve bbox estimated by the dlib_tracker object
		"""
		r = tracker.get_position()
		print "rectangle from dlib:", r
		xmin, ymin, xmax, ymax = self.keep_coords_in_frame([r.left(), r.top(), r.right(), r.bottom()])
		return (int(xmin), int(ymin), int(xmax), int(ymax))

	def tracker_update(self):
		"""
			update image frame for each tracker object
		"""
		for tracker in self.trackers:
			tracker.update(self.img)

	def remove_latest_bbox(self):
		"""
			utility to remove last bbox drawn by user
		"""
		if len(self.bbox) > 0:
			self.bbox = self.bbox[:-1]
			self.img = self.unedited_img.copy()
			self.render_rectangles()

	def viewer(self):
		"""
			renders the UI
		"""

		list_dir = os.listdir(self.path)
		list_dir.sort()
		print "Reading...", len(list_dir)

		for i in range(self.start_from, len(list_dir)):
			if list_dir[i].endswith(self.extension):

				self.window_name = list_dir[i]
				cv2.namedWindow(self.window_name)
				cv2.setMouseCallback(self.window_name, self.on_mouse)

				print self.path + list_dir[i]
				img_filename = list_dir[i]

				self.img = cv2.imread(self.path + list_dir[i])
				self.height, self.width = self.img.shape[:2]
				self.unedited_img = cv2.imread(self.path + list_dir[i])
				cv2.imshow(self.window_name, self.img)


				if True:
					self.tracker_flag = True
					self.tracker_update()
					new_bbox = []
					for i in range(len(self.trackers)):
						box = self.find_box(self.trackers[i])
						new_bbox.append(box)
					self.bbox = new_bbox
					print self.bbox
					self.render_rectangles()

				
				
				key = cv2.waitKey(0) & 0xFF

				# press 'q' to quit the program
				if key == ord('q'):
					break
				
				# press 'n' if the user is unsatisified with the tracker's bboxes
				if key == ord('n'):
					print i
					self.img = self.unedited_img.copy()
					self.tracker_flag = False
					self.bbox = []
					self.render_rectangles()

					while(1):
						key = cv2.waitKey(0) & 0xFF

						# press 'm' if the user has labelled all bboxes and wants to lock the trackers and move to next frame
						if key == ord('m'):
							self.tracker_setup()
							break

						# press 'e' if the user is unsatisified with the latest bbox drawn; erases the latest bbox	
						if key == ord('e'):
							self.remove_latest_bbox()
							
				print img_filename
				print self.bbox

				# call function to write the bbox in VOC style format to an xml file
				# see to_xml.py for more details
				to_xml.generate_xml(img_filename, (self.width, self.height, 4), self.bbox, self.annotation_path)


				

			cv2.destroyAllWindows()


if __name__ == '__main__':
	# pass the ("path/to/img_directory", "path/to/annotation_directory", "image_extension", "image_index_to_begin_from")
	a = annotate("frames/", "annotations/", "png", 0)
	a.viewer()



