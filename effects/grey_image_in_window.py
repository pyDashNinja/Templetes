import cv2
import numpy as np


def grey_image_in_window_vibrate_and_shifts(video_path, start_time, end_time, output_path):
    # Step 1: Extract a frame within the specified time range
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    start_frame = int(start_time * frame_rate)
    end_frame = int(end_time * frame_rate)
    print(cap.get(3), cap.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, frame_rate,
                          (int(cap.get(3)), int(cap.get(4))))

    current_frame = 0
    while True:
        # current_frame +=1
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        if current_frame >= start_frame and current_frame <= end_frame:
            pass

            # Step 2: Convert frame to grayscale
            # grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # # convert grayscale frame to BGRA format
            # grayscale_frame = cv2.cvtColor(
            #     grayscale_frame, cv2.COLOR_GRAY2BGRA)

            # # make a array of grayscale frame height and width size and fill it with 0s
            # mask = np.zeros(
            #     (grayscale_frame.shape[0], grayscale_frame.shape[1]), dtype=np.uint8)

            # # now replace 255 between grayscale_frame.shape[0]*0.2 and grayscale_frame.shape[0]*0.4 with 255 and height  equal to grayscale_frame.shape[1]
            # mask[int(grayscale_frame.shape[0]*0.2):int(grayscale_frame.shape[0]*0.4), :] = 255

            # # where mask is 255 make zero and where it is 0 make 255
            # inverted_mask = cv2.bitwise_not(mask)

            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

            # # apply inverted mask on frame
            # frame = cv2.bitwise_and(frame, frame, mask=inverted_mask)

            # # apply mask on grayscale frame
            # grayscale_frame = cv2.bitwise_and(
            #     grayscale_frame, grayscale_frame, mask=mask)

            # # apply grayscale on top of orignal frame
            # frame = cv2.add(frame, grayscale_frame)

            # Step 6: Apply vibration and blur effects to the window (you can use OpenCV functions)

            # Step 7: Gradually shift the window to the center and repeat the effects

            # Step 8: Continue shifting the window to the left until it reaches the center

            # Step 9: Save the final processed frame to the output_path
        # print(current_frame)
        out.write(frame)
        current_frame += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("successfully saved")

# Example usage:
# apply_effects("input_video.mp4", start_time=10, end_time=15, output_path="output_frame.png")
