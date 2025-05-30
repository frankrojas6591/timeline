# timeline
A set of classes for managing different world historical timelines (list of events).

What start as a minor project to record the events of the early Christian church has evolved into a generic timeline management services.  The idea is not to provide a through or authoriative set of events but a synopsis of events.   You can create your own timeline.txt file for import and graphing. 

## Provides:

- timeline : import timeline (data/timeline-all.txt), find(), slice() and merge() timeline objects
    - impot timeline.txt
    - events have date, prefix, abstract, description
    - prefix help to classify events within timeline, eg. Church, Judeo, Greek, Roman, etc.
- timelineGraph - to build and draw the timeline as a network graph
    - graphs events as nodes  from a "Start of Timeline" (Events).  Events are subdivided per Millenium .

## Import Sources

- Can import a "timeline.txt" file that details a set of historical events (abstract, description).
- import Catholic pope URL to build a timeline-Popes.txt
