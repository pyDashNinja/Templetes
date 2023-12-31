import cv2
import os
import numpy as np

def animated_box(video_path, start_time, end_time, output_path):
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate start and end frame numbers
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Create VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps,
                          (frame_width, frame_height))
    
    # sprite = rounded box, in this function
    sprites = []
    sprites.append(cv2.imread(os.path.join('assets', 'images', 'subscribe2.png'), cv2.IMREAD_UNCHANGED))
    sprites.append(cv2.imread(os.path.join('assets', 'images', 'youtube.png'), cv2.IMREAD_UNCHANGED))
    sprites.append(cv2.imread(os.path.join('assets', 'images', 'youtube.png'), cv2.IMREAD_UNCHANGED))
    sprites.append(cv2.imread(os.path.join('assets', 'images', 'youtube.png'), cv2.IMREAD_UNCHANGED))
    sprites.append(cv2.imread(os.path.join('assets', 'images', 'youtube.png'), cv2.IMREAD_UNCHANGED))

    
    # Loop through the frames and apply the effect
    frame_num = 0
    MAXSIZE = 100
    FINAL_STATE_REACHED_ONCE = False
    FINAL_STATE_REACHED = False

    SIZE = 0
    ANGLE = 180

    SIZE_CHANGE = 3
    ANGLE_CHANGE = 4


    INITIAL_TRANSLATION_CHANGE = 15
    MAX_TRANSLATION = MAXSIZE + MAXSIZE// 4

    # FRAMES_TRANSLATION = MAX_TRANSLATION / INITIAL_TRANSLATION_CHANGE
    # x_array = np.arange(FRAMES_TRANSLATION)
    # exp_values = INITIAL_TRANSLATION_CHANGE * np.exp(-x_array/INITIAL_TRANSLATION_CHANGE * np.log(INITIAL_TRANSLATION_CHANGE))
    # cumulative_sum = np.cumsum(exp_values)
    # normalized_values = exp_values / cumulative_sum[-1]  # Normalize the values to ensure the cumulative sum reaches MAXSIZE
    # result_exp = np.round(normalized_values * MAXSIZE).astype(int)
    # print(result_exp)
    FRAMES_TRANSLATION = MAX_TRANSLATION*2 / INITIAL_TRANSLATION_CHANGE
    DIFFERENCE = INITIAL_TRANSLATION_CHANGE/(FRAMES_TRANSLATION-1)
    result_lin = np.arange(0, INITIAL_TRANSLATION_CHANGE, DIFFERENCE)
    result_lin = np.round(np.array(list((reversed(result_lin))))).astype(int)


    SPRITE_MAX_TRANSLATIONS = [0 if i == 0 else MAXSIZE + MAXSIZE // 4 for i in range(len(sprites))]
    SPRITE_TRANSLATIONS = [0 for i in range(len(sprites))]
    # SPRITE_TRANSLATION_CHANGES = [result_exp[0] for i in range(len(sprites))]
    SPRITE_TRANSLATION_CHANGES = [result_lin[0] for i in range(len(sprites))]

    TRANSLATION_FRAME_NUMBER = 0
    for spriteNum in range(len(sprites)):
        sprites[spriteNum] = changeColor(sprites[spriteNum], [0,0,255,255],[255,255,255,255], [255,255,255])
        if spriteNum != 0:
            sprites[spriteNum] = cv2.resize(sprites[spriteNum], (MAXSIZE,MAXSIZE))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply the effect only within the specified interval
        if start_frame <= frame_num <= end_frame:
            # True only the instance middle sprite reaches final rotation and final size
            if FINAL_STATE_REACHED_ONCE: 
                sprites[0] = changeColor(sprites[0], [255,255,255,255],[0,0,0,255], [255,255,255])
                FINAL_STATE_REACHED = True

            # resized_sprite = cv2.resize(sprite, (SIZE,SIZE))
            resized_sprite = cv2.resize(sprites[0], (SIZE,SIZE))

            # If middle sprite has reached final rotation and final size
            if FINAL_STATE_REACHED:
                # UP = 1
                spriteNumber =  1
                if (TRANSLATION_FRAME_NUMBER < len(result_lin) and result_lin[TRANSLATION_FRAME_NUMBER] == 0) or (SPRITE_TRANSLATIONS[spriteNumber] != SPRITE_MAX_TRANSLATIONS[spriteNumber] and SPRITE_TRANSLATIONS[spriteNumber] + SPRITE_TRANSLATION_CHANGES[spriteNumber] >= SPRITE_MAX_TRANSLATIONS[spriteNumber]):
                    sprites[spriteNumber] = changeColor(sprites[spriteNumber], [255,255,255,255],[0,0,0,255], [255,255,255])
                
                for c in range(0, 3):
                    frame[frame_y-SPRITE_TRANSLATIONS[spriteNumber]:frame_y+sprites[1].shape[0]-SPRITE_TRANSLATIONS[spriteNumber], frame_x:frame_x+sprites[1].shape[1], c] = sprites[1][:, :, c] * (sprites[1][:, :, 3] / 255.0) + frame[frame_y-SPRITE_TRANSLATIONS[spriteNumber]:frame_y+sprites[1].shape[0]-SPRITE_TRANSLATIONS[spriteNumber], frame_x:frame_x+sprites[1].shape[1], c] * (1.0 - sprites[1][:, :, 3] / 255.0)

                # DOWN = 2
                spriteNumber =  2
                if (TRANSLATION_FRAME_NUMBER < len(result_lin) and result_lin[TRANSLATION_FRAME_NUMBER] == 0) or (SPRITE_TRANSLATIONS[spriteNumber] != SPRITE_MAX_TRANSLATIONS[spriteNumber] and SPRITE_TRANSLATIONS[spriteNumber] + SPRITE_TRANSLATION_CHANGES[spriteNumber] >= SPRITE_MAX_TRANSLATIONS[spriteNumber]):
                    sprites[spriteNumber] = changeColor(sprites[spriteNumber], [255,255,255,255],[0,0,0,255], [255,255,255])
                
                for c in range(0, 3):
                    frame[frame_y+SPRITE_TRANSLATIONS[spriteNumber]:frame_y+sprites[1].shape[0]+SPRITE_TRANSLATIONS[spriteNumber], frame_x:frame_x+sprites[1].shape[1], c] = sprites[1][:, :, c] * (sprites[1][:, :, 3] / 255.0) + frame[frame_y+SPRITE_TRANSLATIONS[spriteNumber]:frame_y+sprites[1].shape[0]+SPRITE_TRANSLATIONS[spriteNumber], frame_x:frame_x+sprites[1].shape[1], c] * (1.0 - sprites[1][:, :, 3] / 255.0)

                # LEFT = 3
                spriteNumber =  3
                if (TRANSLATION_FRAME_NUMBER < len(result_lin) and result_lin[TRANSLATION_FRAME_NUMBER] == 0) or (SPRITE_TRANSLATIONS[spriteNumber] != SPRITE_MAX_TRANSLATIONS[spriteNumber] and SPRITE_TRANSLATIONS[spriteNumber] + SPRITE_TRANSLATION_CHANGES[spriteNumber] >= SPRITE_MAX_TRANSLATIONS[spriteNumber]):
                    sprites[spriteNumber] = changeColor(sprites[spriteNumber], [255,255,255,255],[0,0,0,255], [255,255,255])
                
                for c in range(0, 3):
                    frame[frame_y:frame_y+sprites[1].shape[0], frame_x-SPRITE_TRANSLATIONS[spriteNumber]:frame_x+sprites[1].shape[1]-SPRITE_TRANSLATIONS[spriteNumber], c] = sprites[1][:, :, c] * (sprites[1][:, :, 3] / 255.0) + frame[frame_y:frame_y+sprites[1].shape[0], frame_x-SPRITE_TRANSLATIONS[spriteNumber]:frame_x+sprites[1].shape[1]-SPRITE_TRANSLATIONS[spriteNumber], c] * (1.0 - sprites[1][:, :, 3] / 255.0)

                # RIGHT = 4
                spriteNumber =  4
                if (TRANSLATION_FRAME_NUMBER < len(result_lin) and result_lin[TRANSLATION_FRAME_NUMBER] == 0) or (SPRITE_TRANSLATIONS[spriteNumber] != SPRITE_MAX_TRANSLATIONS[spriteNumber] and SPRITE_TRANSLATIONS[spriteNumber] + SPRITE_TRANSLATION_CHANGES[spriteNumber] >= SPRITE_MAX_TRANSLATIONS[spriteNumber]):
                    sprites[spriteNumber] = changeColor(sprites[spriteNumber], [255,255,255,255],[0,0,0,255], [255,255,255])
                
                for c in range(0, 3):
                    frame[frame_y:frame_y+sprites[1].shape[0], frame_x+SPRITE_TRANSLATIONS[spriteNumber]:frame_x+sprites[1].shape[1]+SPRITE_TRANSLATIONS[spriteNumber], c] = sprites[1][:, :, c] * (sprites[1][:, :, 3] / 255.0) + frame[frame_y:frame_y+sprites[1].shape[0], frame_x+SPRITE_TRANSLATIONS[spriteNumber]:frame_x+sprites[1].shape[1]+SPRITE_TRANSLATIONS[spriteNumber], c] * (1.0 - sprites[1][:, :, 3] / 255.0)

                # Update sprite translations
                for spriteNum in range(len(sprites)):
                    if spriteNum == 0: continue

                    SPRITE_TRANSLATIONS[spriteNum] = min(SPRITE_TRANSLATIONS[spriteNum] + SPRITE_TRANSLATION_CHANGES[spriteNum], SPRITE_MAX_TRANSLATIONS[spriteNum])
                
                TRANSLATION_FRAME_NUMBER += 1
                if TRANSLATION_FRAME_NUMBER < len(result_lin):
                    # SPRITE_TRANSLATION_CHANGES = [result_exp[TRANSLATION_FRAME_NUMBER] for i in range(len(sprites))]
                    SPRITE_TRANSLATION_CHANGES = [result_lin[TRANSLATION_FRAME_NUMBER] for i in range(len(sprites))]

            frame_x = (frame.shape[1] - resized_sprite.shape[1]) // 2
            frame_y = (frame.shape[0] - resized_sprite.shape[0]) // 2

            sprite_x = resized_sprite.shape[1] // 2
            sprite_y = resized_sprite.shape[0] // 2

            rotMatrix = cv2.getRotationMatrix2D((sprite_x, sprite_y), ANGLE, 1.0)
            resized_sprite = cv2.warpAffine(resized_sprite, rotMatrix, (resized_sprite.shape[1], resized_sprite.shape[0]))

            # Overlay the second image onto the first image
            for c in range(0, 3):
                frame[frame_y:frame_y+resized_sprite.shape[0], frame_x:frame_x+resized_sprite.shape[1], c] = resized_sprite[:, :, c] * (resized_sprite[:, :, 3] / 255.0) + frame[frame_y:frame_y+resized_sprite.shape[0], frame_x:frame_x+resized_sprite.shape[1], c] * (1.0 - resized_sprite[:, :, 3] / 255.0)

        # Write the modified frame to the output video
        out.write(frame)

        frame_num += 1
        if frame_num % 1 == 0: 
            MAXSIZE_REACHED_ONCE = (SIZE != MAXSIZE)
            MAXANGLE_REACHED_ONCE = (ANGLE != 0)

            SIZE = min(SIZE+SIZE_CHANGE, MAXSIZE)
            ANGLE = max(ANGLE-ANGLE_CHANGE, 0)

            MAXSIZE_REACHED_ONCE = (SIZE == MAXSIZE) and MAXSIZE_REACHED_ONCE
            MAXANGLE_REACHED_ONCE = (ANGLE == 0) and MAXANGLE_REACHED_ONCE

            FINAL_STATE_REACHED_ONCE = MAXSIZE_REACHED_ONCE and (0 == ANGLE)
            FINAL_STATE_REACHED_ONCE = (MAXANGLE_REACHED_ONCE and (MAXSIZE == SIZE)) or FINAL_STATE_REACHED_ONCE
            
    # Release the resources
    cap.release()
    out.release()

    print("The animated box effect has been applied, and the output video is saved at:", output_path)

def customAddWeighted(src1, alpha, src2, beta, gamma=0):
    # Check if the images have the same size
    if src1.shape != src2.shape:
        raise ValueError("Input images must have the same size.")

    # Perform alpha blending
    blended_image = np.clip(src1 * alpha[:, :, np.newaxis] + src2 * beta[:, :, np.newaxis] + gamma, 0, 255).astype(
        np.uint8)

    return blended_image

def changeColor(imgArray, replacement_color_shape, replacement_color_text, target_color_text):
    # target_color_shape = np.array([0,0,0])
    # target_color_shape2 = np.array([1,1,1])
    # target_color_text = np.array([255,255,255])
    target_color_text = np.array(target_color_text)

    replacement_color_shape = np.array(replacement_color_shape)
    replacement_color_text = np.array(replacement_color_text)
    for i in range(len(imgArray)):
        for j in range(len(imgArray[i])):
            # pixel shouldn't be transparent.
            if imgArray[i][j][3] == 0:
                continue

            pixel_shape = True
            pixel_text = True

            for k in range(3):
                # if imgArray[i][j][k] != target_color_shape[k] and imgArray[i][j][k] != target_color_shape2[k]:
                #     pixel_shape = False
                if imgArray[i][j][k] != target_color_text[k]:
                    pixel_text = False

            # if it indeed is shape, change to new shape color
            if not pixel_text:
                imgArray[i][j] = replacement_color_shape
            # if it indeed is text, change to new text color
            else:
                imgArray[i][j] = replacement_color_text

            # if pixel_shape or pixel_text or imgArray[i][j][3] == 0:
            #     continue
            # print(imgArray[i][j])

    # Create a mask for the pixels that match the target color
    # mask1 = np.all((imgArray[...,:3] == target_color), axis=-1)
    # print(mask1.shape)
    # print(imgArray[..., 3].shape)
    # mask2 = np.all((imgArray[...,3] == [0]), axis=-1)
    # print(mask2.shape)

    # # Apply the replacement color to the pixels that match the target color
    # imgArray[mask1] = replacement_color
    return imgArray
