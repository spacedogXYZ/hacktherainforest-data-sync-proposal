HackTheRainforest
=====

Offline Data Sync Proposal
-----

Feb 2015 - Tarapoto, Peru

* Camilo @dedalo
* Josh @jlev


## Problem

The environmental monitoring and mapping application requires full functionality in offline scenarios. Monitors will be taking observations several days travel from towns, and should not be required to send their phones to connect to the internet. Reliable peer-to-peer data & media sync between mobile and management applications is essential.


## User Scenario
Monitors will be equipped with mobile phones running offline web applications will store observations when recorded in a simple key-value store (indexDB, levelDB, or equivalent builtin to Chrome). Managers will have a laptop or Chromebook running a background data-sync service and analysis application.

The laptop or portable hotspot will create a wifi network, so that data-sync can occur without requiring a plug-in connection. 

The manager can view progress and control the data-sync service with a clear web interface, which could also be extended to provide simple filtering and local analysis capabilites  (integrating MapFilter and turf.js).

After syncing recent monitor observations, the manager can export their current database to flat json and media files on an attached drive, for transportation to town, further analysis and syncing, and optional upload to the internet.

![user-scenario-diagram](user-scenario.pdf?raw=true)

## Communication Protocol
Ideally the user should not have to initiate a sync manually, the application should identify peers, copy records, and resolve conflicts manually.

When the monitor app is open and connected to a wireless network, it will send a multicast UDP packet announcing its presence. If the data-sync service is running, it will receive the packet, respond with a packet directed to the client IP with a url scheme for further communication.

The data-sync service will provide a REST API, to which the monitor app will initiate further communications. The monitor app can POST a list of new observation records, or GET a list of changes to download. PUT and DELETE actions should not be allowed by the monitor app.


## Sync Algorithm

To reliably copy observation records with intermittent connections, we have investigated two strategies: use a vector clock to track each node's version history, or compare files solely on a hash of the data. Each has advantages and areas of concern, and more testing is necessary to determine an appropriate solution given our problem constraints.

### Vector Clock
A [vector clock](http://en.wikipedia.org/wiki/Vector_clock) is a method of tracking document versions between nodes, applying partial ordering to determine which has the most recent edit. On starting a sync action, the sending node increments its own counter and sends it along with the data. On accepting a sync, the receiving node increments its own counter and updates every other counter in the vector with the maximum of the value in its own vector clock and the value in the vector in the received message.

In highly-connected systems, this can maintain consistency between temporarily disconnected nodes. In primarily offline systems, extra care will need to be taken to ensure that versions are not lost if a divergence occurs and a descendent chain cannot be determined. This problem is discussed in detail in [why vector clocks are hard](http://basho.com/why-vector-clocks-are-hard/).

One solution to the problem of divergent trees is to track modification time as well as version in each clock, and prune the oldest entries on updating. This avoids adding disconnected versions from old entries, at the cost of potentially increased merge conflicts. Since this system will primarily add records instead of modifying them, this should not be a significant burden on the user.

Good example [python](https://github.com/daviddrysdale/pynamo.git) and [javascript](http://mixu.net/vectorclock/) implementations of vector clocks exist with GPL licenses, and the technique is widely used in "gossip protocols" and distributed databases.

### Hash Comparison

A potentially simpler, but more resource intensive approach is to hash each record on a device, compare each one with every hash on the server, and copy those which are missing in both directions. This will not provide an ordering of edit histories, but that may be possible by comparing file creation and modification times.

_Camilo, add more detail here_ 


## User Interface 