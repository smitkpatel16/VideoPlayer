# UML Class Diagram - VideoPlayer Application

## Overview
This document provides a comprehensive UML class diagram for the VideoPlayer application, showing all classes, their attributes, methods, and relationships.

---

## Class Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PyQt6 Framework Classes                             │
│  (QMainWindow, QWidget, QMediaPlayer, QAudioOutput, QSettings, etc.)        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      △
                                      │ inherits
                    ┌─────────────────┼─────────────────┬──────────────────┐
                    │                 │                 │                  │
                    ▼                 ▼                 ▼                  ▼
        ┌───────────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────────┐
        │  MyVideoPlayer    │ │ MyCentralW.  │ │MyMediaPlayer │ │MyMediaControls │
        ├───────────────────┤ ├──────────────┤ ├──────────────┤ ├────────────────┤
        │ - settings        │ │ - mainLayout │ │ - mediaPlayer│ │ - playButton   │
        │ - playlist        │ │ - layout     │ │ - audioOutput│ │ - stopButton   │
        │ - networktree     │ │              │ │ - videoW.    │ │ - prevBtn      │
        │ - preview         │ │              │ │ - fullScreen │ │ - nextBtn      │
        │ - mediaPlayer     │ │              │ │ - mediaDevs. │ │ - seekSlider   │
        │ - mediaControls   │ │              │ │              │ │ - volumeDial   │
        │ - mainWidget      │ │              │ │              │ │ - durationLbl  │
        │ - hideTimer       │ │              │ │              │ │ - currentLbl   │
        ├───────────────────┤ ├──────────────┤ ├──────────────┤ ├────────────────┤
        │ + __init__()      │ │ + __init__() │ │ + __init__() │ │ + __init__()   │
        │ + keyPressEvent() │ │ + addWidget()│ │ +setMediaFile│ │ + __addControls│
        │ + toggleFS()      │ │ + adjWidgSize│ │ +toggleFS()  │ │ + __addLabels()│
        │ + __addMenuBar()  │ │ + eventFilter│ │ +adjustVol() │ │ +__playPauseCh.│
        │ + __addMPWidget() │ │              │ │ +eventFilter │ │ + __arrangeW.  │
        │ + __connectMC()   │ │              │ │ +isFullScreen│ │ + updateSlider │
        │ + previewDisplay()│ │              │ │ +videoWidget │ │ + __setPrev()  │
        │ + __playFile()    │ │              │ │              │ │ + __setNext()  │
        │ + __displayReelC()│ │              │ │              │ │               │
        │ + manageControl() │ │              │ │              │ │               │
        │ + showPlaylist()  │ │              │ │              │ │               │
        │ + showNetwork()   │ │              │ │              │ │               │
        │ + __openFileD()   │ │              │ │              │ │               │
        │ + playNetworkURL()│ │              │ │              │ │               │
        └───────────────────┘ └──────────────┘ └──────────────┘ └────────────────┘
                    │                 △                 △                  △
                    │ contains        │ contains        │ contains         │
                    └─────────────────┴─────────────────┴──────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                       Playlist Component Classes                              │
└─────────────────────────────────────────────────────────────────────────────┘
        
    ┌──────────────────┐         ┌─────────────────┐
    │MyPlaylistItem    │         │  MyPlaylist     │
    ├──────────────────┤         ├─────────────────┤
    │ - displayText    │         │ - mainWidget    │
    │ - fullPath       │         │                 │
    ├──────────────────┤         ├─────────────────┤
    │ + __init__()     │         │ + __init__()    │
    │                  │         │ + addPLItem()   │
    │                  │         │ + setActiveItem │
    │                  │         │ + setPrev()     │
    │                  │         │ + setNext()     │
    └──────────────────┘         └─────────────────┘
            △                             △
            │ parent                      │ contains
            │                             │
        (QListWidgetItem)         (QMainWindow)


┌─────────────────────────────────────────────────────────────────────────────┐
│                    Network Component Classes                                  │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────┐         ┌─────────────────┐
    │MyNetworkItem     │         │ MyNetworkTree   │
    ├──────────────────┤         ├─────────────────┤
    │ - displayText    │         │ - mainWidget    │
    │ - browse         │◄────────│ - treeWidget    │
    │ - itemID         │         │                 │
    │ - address        │         ├─────────────────┤
    ├──────────────────┤         │ + __init__()    │
    │ + __init__()     │         │ + addParentItem │
    │                  │         │ + addChildItem  │
    │                  │         │ + getParent()   │
    │                  │         │ - __itemClicked │
    │                  │         │                 │
    │                  │         │ [Signal]        │
    │                  │         │ - playMediaFile │
    └──────────────────┘         └─────────────────┘
            △                             △
            │ parent                      │
            │                             │
        (QTreeWidgetItem)        (QMainWindow)


┌─────────────────────────────────────────────────────────────────────────────┐
│                     UI Component Classes                                      │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────┐         ┌──────────────────┐
    │   MySlider       │         │   MyPreview      │
    ├──────────────────┤         ├──────────────────┤
    │ - duration       │         │ - view           │
    │ - __inside       │         │ - display        │
    │ - __sentStamp    │         │ - position       │
    ├──────────────────┤         │ - mainLayout     │
    │ + __init__()     │         ├──────────────────┤
    │ + mouseMoveEvent │         │ + __init__()     │
    │ + enterEvent()   │         │ + showImage()    │
    │ + leaveEvent()   │         │                  │
    │                  │         │ [Signal]         │
    │ [Signals]        │         │ - (none)         │
    │ - showPreview    │         └──────────────────┘
    │ - enterPreview   │              △
    │ - exitPreview    │              │
    └──────────────────┘          (QDialog)
            △
            │
        (QSlider)

    ┌──────────────────┐
    │MyThumbnailDisplay│
    ├──────────────────┤
    │ - display        │
    │ - __pen          │
    │ - __count        │
    │ - __totalW       │
    │ - __duration     │
    │ - __r            │
    ├──────────────────┤
    │ + __init__()     │
    │ + clearDisplay() │
    │ + addImage()     │
    │ + setDuration()  │
    │ + setPosition()  │
    └──────────────────┘
            △
            │
      (QGraphicsView)


┌─────────────────────────────────────────────────────────────────────────────┐
│                   Processing/Utility Classes                                  │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────┐         ┌──────────────────┐
    │ExtractImages     │         │PreviewPosition   │
    ├──────────────────┤         ├──────────────────┤
    │ - fPath          │         │ - fPath          │
    │ - split          │         │ - capture        │
    │ - pos            │         │ - frameCount     │
    │ - capture        │         │ - r              │
    │ - frameCount     │         ├──────────────────┤
    │ - frameInterval  │         │ + __init__()     │
    │ - _readVideo     │         │ + extract()      │
    ├──────────────────┤         └──────────────────┘
    │ + __init__()     │              △
    │ + baselineRead() │              │
    │ + _transmitFrame │           (object)
    │ + run()          │
    │                  │         ┌──────────────────┐
    │ [Signals]        │         │SelectionLine     │
    │ - reelImage      │         ├──────────────────┤
    │ - finished       │         │ (attributes of   │
    │ - over           │         │  QGraphicsLine)  │
    └──────────────────┘         ├──────────────────┤
            △                    │ + __init__()     │
            │                    │ + itemChange()   │
        (QObject)                │ + hoverEnterEvent
                                 │ + hoverLeaveEvent
                                 │                  │
                                 │ [Signal]         │
                                 │ - updateHighlight│
                                 └──────────────────┘
                                         △
                                         │
                                 (QGraphicsLineItem)


┌─────────────────────────────────────────────────────────────────────────────┐
│                    Utility Functions (processTools.py)                        │
└─────────────────────────────────────────────────────────────────────────────┘

    • extractAudio(filePath)        - Extract audio from video file
    • checkDuration(filePath)       - Get duration of video file
    • checkDurationAudio(filePath)  - Get duration of audio file
    • browseChildren(parentID, browse) - Browse network device children


```

---

## Relationship Summary

### Composition (Contains)
- `MyVideoPlayer` **contains**: `MyCentralWidget`, `MyMediaPlayer`, `MyMediaControls`, `MyPlaylist`, `MyNetworkTree`, `MyPreview`
- `MyCentralWidget` **contains**: Layout and child widgets
- `MyMediaPlayer` **contains**: `QMediaPlayer`, `QAudioOutput`, `QVideoWidget`
- `MyMediaControls` **contains**: `MySlider`, `QPushButton`, `QDial`, `QLabel`
- `MyPlaylist` **contains**: `QListWidget` with `MyPlaylistItem` items
- `MyNetworkTree` **contains**: `QTreeWidget` with `MyNetworkItem` items
- `MyThumbnailDisplay` **contains**: `QGraphicsScene`
- `MyPreview` **contains**: `QGraphicsView`, `QGraphicsScene`, `QLabel`

### Inheritance
- `MyVideoPlayer` **extends**: `QMainWindow`
- `MyCentralWidget` **extends**: `QWidget`
- `MyMediaPlayer` **extends**: `QWidget`
- `MyMediaControls` **extends**: `QWidget`
- `MySlider` **extends**: `QSlider`
- `MyPlaylist` **extends**: `QMainWindow`
- `MyPlaylistItem` **extends**: `QListWidgetItem`
- `MyNetworkTree` **extends**: `QMainWindow`
- `MyNetworkItem` **extends**: `QTreeWidgetItem`
- `MyPreview` **extends**: `QDialog`
- `MyThumbnailDisplay` **extends**: `QGraphicsView`
- `ExtractImages` **extends**: `QObject`
- `SelectionLine` **extends**: `QGraphicsLineItem`

### Signal Connections
- `MyMediaControls` **signals**: `playMedia`, `pauseMedia`, `prev`, `next`
- `MySlider` **signals**: `showPreview`, `enterPreview`, `exitPreview`
- `MyNetworkTree` **signals**: `playMediaFile`
- `ExtractImages` **signals**: `reelImage`, `finished`, `over`
- `SelectionLine` **signals**: `updateHighlight`

---

## Key Methods by Class

### MyVideoPlayer (Main Application)
- Application initialization and event handling
- Menu bar setup
- Media control connections
- File dialog management
- Network device discovery
- Full-screen management
- Preview display coordination

### MyMediaPlayer
- Video playback control
- Volume management
- Full-screen toggling
- Media file loading

### MyMediaControls
- Play/Pause button management
- Seek slider control
- Volume dial management
- Duration display

### MyPlaylist
- Playlist item management
- Current item tracking
- Navigation (previous/next)

### MyNetworkTree
- UPnP device browsing
- Network content navigation
- Media file selection from network

### Processing Classes
- `ExtractImages`: Multi-threaded frame extraction from videos
- `PreviewPosition`: Single frame extraction at specific timestamps
- `SelectionLine`: Graphics item for timeline navigation

---

## Data Flow

```
User Input (Menu/Buttons)
        ↓
MyVideoPlayer (Event Handler)
        ↓
MyMediaControls (Signal Emitter)
        ↓
MyMediaPlayer (Playback Control)
        ↓
QMediaPlayer (PyQt6 Core)
        ↓
Audio/Video Output

Preview Request
        ↓
MySlider (showPreview Signal)
        ↓
PreviewPosition (Extract Frame)
        ↓
MyPreview (Display)
```

---

## Technical Stack

- **Framework**: PyQt6
- **Video Processing**: OpenCV (cv2)
- **Audio Processing**: FFmpeg, Wave module
- **Network Protocol**: UPnP (upnpy)
- **XML Parsing**: lxml

---

## File Organization

```
VideoPlayer/
├── Main.py                  # Main application class (MyVideoPlayer)
├── MyCentralWidget.py       # Central widget container
├── MyMediaPlayer.py         # Media playback engine
├── MyMediaControls.py       # Media control UI
├── MySlider.py              # Custom slider with preview
├── MyPlaylist.py            # Playlist management
├── MyNetworkTree.py         # Network device browsing
├── MyPreview.py             # Preview dialog
├── MyThumbnailDisplay.py    # Thumbnail display
├── processTools.py          # Video/audio processing utilities
├── neighbourhood.py         # (Not analyzed in diagram)
├── requirements.txt         # Dependencies
└── testBench/               # Test files
```

---

## Architecture Pattern

The VideoPlayer application follows a **Model-View-Controller (MVC)** pattern:

- **Model**: `ExtractImages`, `PreviewPosition`, file/network data management
- **View**: `MyMediaPlayer`, `MyMediaControls`, `MyPlaylist`, `MyNetworkTree`, `MyPreview`, `MySlider`
- **Controller**: `MyVideoPlayer` (Main application orchestrating all components)

