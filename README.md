# Acetone

k**A**bs**C**h algorithm based sup**E**rposition **T**ool f**O**r ble**N**d**E**r

Use Kabsch algorithm to superimpose two objects in blender based on selected points. This should be used when only some points of two objects can be superimposed but the rest of the object is to different.

## Installation
To install acetone, follow these steps:
*   Download the repository by cloning it or downloading the ZIP file.
*   Open Blender and navigate to Edit > Preferences > Add-ons.
*   Click on Install and select the downloaded repository or ZIP file.
*   Enable the add-on by checking the box next to acetone.

## Usage
In order to align two objects based on the selected points the following steps need to be taken (the images referred to are located [here](https://github.com/gwirn/acetone/tree/master/assets)):
*   Switch to `edit mode`
*   Select points of the static (**not moved**) object ([separate](https://github.com/gwirn/acetone/tree/master/assets/separate.png) left side) `A` > `B` > `C`
*   Select points of the mobile (**moved**) object ([separate](https://github.com/gwirn/acetone/tree/master/assets/separate.png) right side) `A` > `B` > `C` - **so that the corresponding points in the objects are selected in the same order (`A left` to `A right`, `B left` to `B right`, `C left` to `C right`)**
*   Press n and go to the `acetone` header
*   Press `Superimpose`

This will calculate the optimal rotation matrix based on the [Kabsch algorithm](https://en.wikipedia.org/wiki/Kabsch_algorithm) and update the coordinates of the `mobile object` so they align with the `static object` and are [superimposed](https://github.com/gwirn/acetone/tree/master/assets/superimposed.png).

## Output
**RMSD:** Root mean squared deviation between the selected aligned points to judge the superposition quality.
