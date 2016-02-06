from django.http import HttpResponse
import vlc
from ctypes import *
import os
from os import listdir
from os.path import isfile, join

def queue(request):
    path = request.GET.get('path','')#Pluck the path given in URL
    directory = getDirectoryFromPath(path)#Get relative directory
    directoryFiles = getFilesFromDirectory(directory)#Get all of the files in relative directory

    pathList = vlc.libvlc_media_list_new(libvlc)# init list to be added

    for i in range(0, len(directoryFiles)):
        if path != directory + directoryFiles[i]: #Do not add the file we already added
            addFileToMediaList(pathList, addFile(libvlc, directory + directoryFiles[i]))#Add file to Media List

    addFileToMediaList(pathList, addFile(libvlc, path))#Add file to Media List

    vlc.libvlc_media_list_player_set_media_list(mediaListPlayer, pathList)#set medialistplayer's list
    vlc.libvlc_media_list_player_play(mediaListPlayer)#start playing the list
    
    return HttpResponse(path)

def play(request):
    origState = vlc.libvlc_media_list_player_get_state(mediaListPlayer)
    vlc.libvlc_media_list_player_play(mediaListPlayer)
    newState = vlc.libvlc_media_list_player_get_state(mediaListPlayer)
    return HttpResponse(showStateProgress(origState, newState))

def stop(request):
    origState = vlc.libvlc_media_list_player_get_state(mediaListPlayer)
    vlc.libvlc_media_list_player_stop(mediaListPlayer)
    newState = vlc.libvlc_media_list_player_get_state(mediaListPlayer)
    return HttpResponse(showStateProgress(origState, newState))

def pause(request):
    origState = vlc.libvlc_media_list_player_get_state(mediaListPlayer)
    vlc.libvlc_media_list_player_pause(mediaListPlayer)
    newState = vlc.libvlc_media_list_player_get_state(mediaListPlayer)
    return HttpResponse(showStateProgress(origState, newState))

def next(request):
    origState = vlc.libvlc_media_list_player_get_state(mediaListPlayer)
    vlc.libvlc_media_list_player_next(mediaListPlayer)
    newState = vlc.libvlc_media_list_player_get_state(mediaListPlayer)
    return HttpResponse(showStateProgress(origState, newState))

def prev(request):
    origState = vlc.libvlc_media_list_player_get_state(mediaListPlayer)
    vlc.libvlc_media_list_player_previous(mediaListPlayer)
    newState = vlc.libvlc_media_list_player_get_state(mediaListPlayer)
    return HttpResponse(showStateProgress(origState, newState))

#Gets the containing directory given a file path
def getDirectoryFromPath(path):
    arr = path.split(os.sep)#seperate the folders based on os 
    size = len(arr) - 1
    dir = r''
    for i in range(0, size):
        dir += arr[i] + os.sep
    return dir

#Returns all files in a given directory
def getFilesFromDirectory(directory):    
    return [f for f in listdir(directory) if isfile(join(directory, f))]


#Returns a libvlc_media_t*
def addFile(libvlc, path):
    return vlc.libvlc_media_new_path(libvlc, path.encode())
      
#Returns 0 on success, -1 if the media list is read-only
def addFileToMediaList(list, item, index = 0):
    return vlc.libvlc_media_list_insert_media(list, item, index)

#returns the previous and current state
def showStateProgress(prevState, newState):
    return str(prevState) + "------->" + str(newState)

#initialize
libvlc = vlc.libvlc_new(0, None)# init libvlc
mediaListPlayer = vlc.MediaListPlayer()#set media List player
