# A quick readme
I jumped in to revive a stale codebase because league is starting so soon! We'd love to release the source, but th original author is MIA, so waiting to hear back for source release details if possible. We want to respect the originators efforts, and respect your decision to use or not to use this app in the mean time.


Steps/Notes/Advice/Info
1) You can clone the repo as is, or download the zip file from the releases. Everything should be in the same folder as the exe.
2) Open up the Setup.ini file in text editor and *please read the instructions in that file*. There is info you need to fill out or else it won't work. Most importantly your poe account name and your POESESSID.
3) It assumes the OS is Windows 10 and your filter folder is the default path "Documents\My Games\Path of Exile". I wouldn't mess with the included filter at this point in time. The app recreates the included default on start up, if it is not detected in your filters folder, and saves it to your filters folder. Each time you refresh or highlight chaos recipe items, it will update this filter file. So you will then need to refresh the filters in game to see changes.
4) It's not instant. Unfortunately there's going to be some lag between the online stash and the app synchronization/refresh. It won't keep up with how quickly you are making exalts.
5) It should work with any screen resolution, but have seen some issues crop up. If you are running two monitors, it is going to show up on Screen 0, so run PoE in Windowed Fullscreen on your primary monitor.

----
Updates
-----

* If your account name contains non-ASCII characters, you must URL encode it first here: https://www.urlencoder.org/ Example: username Đãřķ becomes %C4%90%C3%A3%C5%99%C4%B7 after URL encoding and that can be used in the setup.ini

* By default, only *unidentified* rare items item level 64 and 75 will be highlighted. This can be changed in the `chaos_items_filter.filter` file.

* There are two numbers in the overlay for each item class: #1/#2 where #1 is the number of unidentified items of that class were found in the stash tab, and #2 is how many identified items were found in the stash tab (within the item level range mentioned above).

* You will need to click the 'Chaos Recipe' button to cycle through highlights for each complete set. The number of sets highlighted can be customized by the `highlight_max_num_sets` parameter in the `Setup.ini` file.

* Please try the latest files if you are having issues after successfully being able to launch the app the first time.

* There is no need to copy anything into your "Documents\My Games\Path of Exile\", since this is done for you the first time. If you need to reset the filter for any reason, you can remove the filter that was added to your "Documents\My Games\Path of Exile\" folder. Don't delete the filters that come with the executable.

* Color scheme should be colorblind friendly!

* If you'd like to use this too in ssf, you can try to change the league to "ssf standard" (no quotation marks for now)
