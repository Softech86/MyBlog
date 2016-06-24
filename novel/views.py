from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from novel.models import Novel, Chapter, SourceStage
from django.db.models import Q

import datetime, queue, threading

from novel_crawer.crawer import multyThread, Novel as CrawerNovel, Chapter as CrawerChapter, ResourcePage

def novel_list(request):
    if request.method == 'GET':
        novels = Novel.objects.all().order_by("-last_update_timestamp")
        stages = SourceStage.objects.all()
        for n in novels:
            chapters = Chapter.objects.filter(novel = n).order_by('-chapter_id')
            if chapters:
                n.latest_chapter = chapters[0].chapter_order + ' - ' + chapters[0].title
                n.latest_chapter_id = chapters[0].chapter_id
                n.last_update_timestamp = chapters[0].last_update_timestamp
            else:
                n.latest_chapter = '暂无章节'
                n.latest_chapter_id = ''
                n.last_update_timestamp = n.create_timestamp
            n.save()
        return render(
            request,
            "novel_list.html",  
            {"novels": novels, "stages": stages},
            context_instance = RequestContext(request)
        )
    else:
        print(request.POST)
        name = request.POST['name'].strip()
        author = request.POST['author'].strip()
        yisou_id = request.POST['yisou_id'].strip()
        resource = request.POST['resource'].strip()
        new_novel = Novel(
            name = name,
            author = author,
            desc = '',
            yisou_id = yisou_id,
            latest_chapter = '',
            latest_chapter_id = -1,
            last_update_timestamp = datetime.datetime.now(),
            resource = resource
        )
        new_novel.save()
        return redirect(reverse("novel_list"))
    
def novel_index(request, novel_id):
    novel = Novel.objects.get(id = novel_id)
    yisou_id = str(novel.yisou_id)
    chapters = Chapter.objects.filter(novel = novel).order_by('-chapter_id')
    offered_stages = [x[1] for x in ResourcePage(yisou_id).resources]
    stage_available = novel.resource in offered_stages
    stages = SourceStage.objects.filter(name__in = offered_stages)
    if request.method == 'GET':
        return render(
            request,
            "novel_index.html",
            {'novel': novel, 'chapters': chapters, 'stages': stages, 'stage_available': stage_available},
            context_instance = RequestContext(request)
        )
    else:
        print(request.POST)
        
        if len(request.POST) == 2:
            novel.resource = request.POST['site_name']
            chapters = Chapter.objects.filter(Q(novel = novel))
            print(len(chapters))
            for c in chapters:
                c.delete()
            #input()
        
        crawernovel = CrawerNovel(yisou_id, novel.resource)
        novel.desc = crawernovel.desc
        novel.save()
        mutex = threading.Lock()
        @multyThread
        def download(chapterOrder):
            #print(chapterOrder, type(chapterOrder))
            chapter = crawernovel.getChapter(chapterOrder, watch = False)
            if chapter:
                newChapter = Chapter(
                    novel = novel,
                    chapter_id = chapter.titleInfo['chapter_id'], 
                    chapter_order = chapter.titleInfo['chapter_order'], 
                    title = chapter.titleInfo['part_name'] + chapter.titleInfo['chapter_title'], 
                    content = ''.join(['<p><span style = "opacity: 0;">____</span>' + x + '</p>' for x in chapter.content])
                )
                if mutex.acquire(1):
                    newChapter.save()
                mutex.release()
        
        #chapterInfo = chapters.values('title', 'chapter_id', 'chapter_order')
        titleInfoOnLine = [CrawerChapter.analyzeTitle(x[1]) for x in crawernovel.res[0][1]]
        idQueue = queue.Queue()
        for i in titleInfoOnLine[:]:#TODO: multy thread and change ip to improve crawer
            title = ''.join(filter(lambda x: x, [i['part_name'], i['chapter_title']]))
            #print(title)
            c = chapters.filter(Q(title = title) & Q(chapter_id = i['chapter_id']))
            if c:
                titleInfoOnLine.remove(i)
            else:
                #download(int(i['chapter_id']) - 1)
                idQueue.put((int(i['chapter_id']) - 1, ))
        
        download(100, idQueue)
        
        chapters = Chapter.objects.filter(novel = novel).order_by('-chapter_id')
        return render(
            request,
            "novel_index.html",
            {'novel': novel, 'chapters': chapters, 'stages': stages, 'stage_available': True},
            context_instance = RequestContext(request)
        )
            
def novel_chapter_display(request, novel_id, chapter_id):
    novel = Novel.objects.get(id = novel_id)
    chapter = Chapter.objects.filter(Q(chapter_id = chapter_id) & Q(novel = novel))[0]
    next_chapter = (Chapter.objects.filter(Q(chapter_id = str(int(chapter_id) + 1)) & Q(novel = novel)) or [''])[0]
    pre_chapter = (Chapter.objects.filter(Q(chapter_id = str(int(chapter_id) - 1)) & Q(novel = novel)) or [''])[0]
    #next_chapter = pre_chapter = ""
    #print('2', next_chapter, pre_chapter, '3')
    
    return render(
        request,
        "novel_chapter_display.html",
        {'novel': novel, 'chapter': chapter, 'next_chapter': next_chapter, 'pre_chapter': pre_chapter},
        context_instance = RequestContext(request)
    )