Use Megadetector to process all the images – it will label humans, animals, and vehicles.
    - Download “megadetector_v2.pb” file
    - Run the “run_tf_detector_batch.py” script
    - Try to do this on GPU
    - Generally I provided the output file as “output.json” (there are other formats you can choose from as well). Please use json output if you are trying to work with my scripts.

If you want to go through all the labels output from Megadetector manually (recommended if small number of images / if you have time, because megadetector will often have quite a few false positives, like rocks or plants labelled as animals) then use my manual_labels.py script, which will display the labels one by one.
    The script will display a bounding box and ask “is this wrong?” If it isn’t wrong, just press enter. If it IS wrong, then press “y” and my script will automatically discount that label.

If you want a visualization of all the labels, use my visualize.py script
