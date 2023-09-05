import cv2
import numpy as np
import time
class CentroidTracker:
    def __init__(self, max_distance=50):
        self.max_distance = max_distance  # Maximum distance to associate centroids
        self.next_object_id = 0  # ID for the next tracked object
        self.objects = {}  # Dictionary to store tracked objects

    def register(self, centroid):
        # Register a new object with a unique ID
        self.objects[self.next_object_id] = centroid,time.time()
        self.next_object_id += 1

    def deregister(self, object_id):
        # Deregister an object by removing it from the dictionary
        del self.objects[object_id]

    def update(self, centroids):
        # Find centroids of objects in the current frame (e.g., using object detection)
        # In this example, we assume that centroids are provided as a list of (x, y) coordinates
        
        # If no centroids are found, deregister all objects
        if len(self.objects.keys()) == 0:
            for centroid in centroids:
                self.register(centroid)
        else:
            # Initialize a list of object IDs and associated distances
            object_ids = list(self.objects.keys())
            object_distances = []

            # Calculate distances between the centroids and existing objects
            for centroid in centroids:
                distances = [np.sqrt((centroid[0] - self.objects[obj_id][0][0]) ** 2 +
                                     (centroid[1] - self.objects[obj_id][0][1]) ** 2) for obj_id in object_ids]
                min_distance = min(distances)
                object_distances.append(min_distance)

            # Find the centroid with the minimum distance for each object
            used_objects = set()

            for _ in range(len(centroids)):
                min_distance_idx = np.argmin(object_distances)
                object_id = object_ids[min_distance_idx]

                if object_distances[min_distance_idx] < self.max_distance:
                    self.objects[object_id] = centroids[min_distance_idx],time.time()
                    used_objects.add(object_id)
                else:
                    self.register(centroid)

                object_distances[min_distance_idx] = float('inf')

            # Deregister objects that were not associated with any centroids
            unused_objects = set(object_ids) - used_objects
            for object_id in unused_objects:
                last_time = self.objects[object_id][-1]
                if (time.time()-last_time)>3:
                    self.deregister(object_id)

        # # Draw bounding boxes and object IDs on the frame for visualization (optional)
        # for object_id, centroid in self.objects.items():
        #     x, y = centroid
        #     cv2.putText(frame, f"ID {object_id}", (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        #     cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

        return self.objects

# Example usage
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    centroid_tracker = CentroidTracker()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        tracked_frame = centroid_tracker.update(frame)
        cv2.imshow("Centroid Tracking", tracked_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
