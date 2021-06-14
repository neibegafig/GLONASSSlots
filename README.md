# GLONASSSlots
This was a small program I wrote that takes the Constellation Status table from the [Information and Analysis Center website](https://www.glonass-iac.ru/en/GLONASS/) in a format for easy value access. Requires an active internet connection to work. You may need to install a few repositories first to include: requests, time, numpy, sys, and datetime. In essence this is just a text parser that downloads the html from the website and parses through to only grab information related to the table found in the link. Currently this is as of 14 June 2021, if website changes its formatting at all then this will too have to change. Everything here is already called when you run the program. If you want to view the data, simply type in the console "

```
GlonassSlots    # Will give you list of all current glonass slots based off of the txt document downloaded
SlotToGC        # Will give you the slot number to GC as a table.
```

This was done for one of my projects that is working with Rinex observation data. I made it because I was having trouble finding an appropriate medium to get orbit slot number (as described in rinex documentation) to GC/Norad ID. If any trouble loading this please let me know and I will try to fix in time. Thanks!
