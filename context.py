import sys
import xbmc
import xbmcaddon
import xbmcgui

def main():
    if xbmc.getCondVisibility('Container.Content(tvshows)'):
        mediatype = 'tvshow'
    elif xbmc.getCondVisibility('Container.Content(movies)'):
        mediatype = 'movie'
    elif xbmc.getCondVisibility('Container.Content(episodes)'):
        mediatype = 'episode'
    elif xbmc.getCondVisibility('Container.Content(musicvideos)'):
        mediatype = 'musicvideo'
    else:
        xbmc.executebuiltin('Notification(Select Artwork to Download cannot proceed, "Got an unexpected content type. Try again, it will probably work.", 6000, DefaultIconWarning.png)')
        return

    infolabel = xbmc.getInfoLabel('ListItem.Label')
    truelabel = sys.listitem.getLabel()
    mismatch = infolabel != truelabel
    if mismatch:
        log("InfoLabel does not match selected item: InfoLabel('ListItem.Label'): '%s', sys.listitem '%s'" % (infolabel, truelabel), xbmc.LOGWARNING)
        dbid = get_realdbid(sys.listitem)
    else:
        dbid = xbmc.getInfoLabel('ListItem.DBID')

    artworkaddon = xbmcaddon.Addon().getSetting('artwork_addon')
    if not xbmc.getCondVisibility('System.HasAddon({0})'.format(artworkaddon)):
        xbmcgui.Dialog().ok('Select Artwork to Download', "The add-on {0} is not installed. Please install it or configure this context item to use another add-on.".format(artworkaddon))
        return
    xbmc.executebuiltin('RunScript({0}, mode=gui, mediatype={1}, dbid={2})'.format(artworkaddon, mediatype, dbid))

    if mismatch:
        xbmc.sleep(1000)
        xbmc.executebuiltin('Notification(Corrected InfoLabel mismatch, "Real: %s, InfoLabel: %s", 6000, DefaultIconInfo.png)' % (truelabel, infolabel))

def get_realdbid(listitem):
    return listitem.getfilename().split('?')[0].rstrip('/').split('/')[-1]

def log(message, level=xbmc.LOGNOTICE):
    xbmc.log('[context.artwork.downloader.gui] %s' % message, level)

if __name__ == '__main__':
    main()
