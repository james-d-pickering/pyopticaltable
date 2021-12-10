PyOpticalTable : Pain-Free Drawing of Optical Setups
======================================================================================

Overview
-----------------------

**PyOpticalTable** is a Python library designed to make it easy to create high-quality figures of optical setups, for use in papers, theses, or presentations. The figure creation is all done using `matplotlib <www.matplotlib.org>`, and **PyOpticalTable** essentially provides a user-friendly syntax for drawing the setup. 

.. figure:: ./complex_example.png
    :width: 800px

    Click image for the high-res version.

Why bother when Inkscape exists?
-------------------------------------

Anyone who has used inkscape to try and draw a complex optical setup will probably have experienced the following:

* Clicking and dragging things to place the optics is easy initially 
* Actually getting it to be precise, so that it looks professional, is harder.
* When you need to adjust the position of an optic because a proof-reader corrected it, it's a complete pain to readjust all the subsequent beam routing.
* When you need to resize the figure because the journal you're submitting to don't understand LaTeX, it makes everything look odd because the aspect ratio can change. 
* Inkscape periodically will crash and freeze for no explicable reason.

So whilst Inkscape (or another point-and-click graphics editor) is easy to use at the start, it quickly becomes the bane of your existence. **PyOpticalTable** solves the problems listed above:

* Using PyOpticalTable, you can place all the optics precisely using a coordinate system that is logical and intuitive - and you can set a temporary grid over the table to make finding the coordinates very easy. 
* Using PyOpticalTable, the trajectory of the laser beam(s) is defined *by the position of the optics*, just like on a real optical table. So if you move an optic, the beam trajectory automatically reroutes itself to compensate.
* Using PyOpticalTable, all the graphics for the pre-defined optical elements will maintain their appearance if you change the figure size, aspect ratio, or rotation. So whatever you need to do to make the figure fit into where you want it, you won't have to spend ages updating all of the individual components on the figure.
* Python IDEs freeze less often than inkscape (although this admittedly depends on IDE choice. Use vim for the sleekest experience.)

The downsides of PyOpticalTable are:

* Using PyOpticalTable will mean there's a bit of a learning curve if you don't already know Python.
* If your optical setup is very simple (like, two mirrors and a box simple), then maybe it's quicker to just use Inkscape. 

Scope 
---------------------

Currently the inbuilt optics in PyOpticalTable include mirrors, beamsplitters, lenses, waveplates (any kind of flat transmissive plate - crystals, windows...), and polarisers. Also available are ways to make lasers (\'box\' sources), and generic point sources where beams can come from. Things like beam dumps are also included. There are a variety of helper functions and routines that make adding/creating your own specific optical elements straightforward too - most things are built up from simpler elements like line objects or arc patches. 

PyOpticalTable currently only deals with perfect laser beams, and so there isn't any native way to draw a diverging beam that has a realistic divergence affected by a lens (although this can be approximated by using two LaserBeam objects). It is *not* a ray tracing program, and has been designed around making professional-looking figures for publications/theses - not for accurately simulating all of the optical physics.

