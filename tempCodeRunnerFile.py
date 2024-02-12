transcript_obj = get_transcript_object(video_id)
    subtitle_lst = []
    for element in transcript_obj:
        subtitle = element['text']
        subtitle_lst.append(subtitle)
    return subtitle_lst