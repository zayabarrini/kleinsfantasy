blender --background \
        --python animated_klein.py \
        --render-output /home/zaya/Downloads/Animations/klein_%04d.png \
        --engine CYCLES \
        --render-anim \
        --enable-autoexec

ffmpeg -i /home/zaya/Downloads/Animations/klein_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4