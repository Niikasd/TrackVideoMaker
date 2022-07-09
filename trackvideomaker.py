import cairo
import json
import datetime
#Make sure no names in name_list contain special charactsers (a-z, numbers, and common punctuation will work fine).
#The program wont break from names longer than 12 characters but after that some names will not fit in the allotted space.
from names_colors import name_list
from names_colors import colourlists

#select track ID, initialize the first and last wrs
track_select = '7'
title = "Roo's Top 10 Every Week"
firstwr = 7000
currentwr = 5651
#select number of displayed times
displayed_times = 10
#initializing some date variables
start_date = 0
end_date = 0
duration = 0
current_date = 0
day_count = 0
week_count = 0
day_cycle = 65
move_cycle = 24
#data=all the data, track_data=data we will use this time 
data = []
track_data = []
#ranked_times are all currently ranked times
ranked_times = {}
#top_10 is the current top 10
top_10 = []
old_top = []
#initializing some time units
hour = 3600
day = 24*hour
week = day*7
#list of users
lengths = [[0]]*1000

def main():
	#loading background photo
	for e in range (day_cycle):
		ims = cairo.ImageSurface.create_from_png("background.png")
		cr = cairo.Context(ims)
		cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
			cairo.FONT_WEIGHT_NORMAL)
		cr.set_font_size(35)
		#setting up font 
	#adding a transparent filter to make the background darker
		cr.set_source_rgba(0.1, 0.1, 0.2, 0.5)
		cr.rectangle(0, 0, 1920, 1080)
		cr.fill()
		gap = firstwr - currentwr
 		#preventing divisioni by zero error
		for ii in range(displayed_length):
			lengths[ii] = (top_10[ii]['SCORE'] - currentwr)/gap
			if e<move_cycle:
				pos = ((top_10[ii]['PRERANK']*(move_cycle-e))+ (top_10[ii]['RANK']*e))/move_cycle - 1
				if top_10[ii]['PRERANK'] != top_10[ii]['RANK']:
					cr.set_source_rgba(colourlists[top_10[ii]['COUNTRY']][0][0]/255, colourlists[top_10[ii]['COUNTRY']][0][1]/255, colourlists[top_10[ii]['COUNTRY']][0][2]/255, 0.3)
				else:
					cr.set_source_rgba(colourlists[top_10[ii]['COUNTRY']][0][0]/255, colourlists[top_10[ii]['COUNTRY']][0][1]/255, colourlists[top_10[ii]['COUNTRY']][0][2]/255, 1)
			else:
				pos = ii
				cr.set_source_rgba(colourlists[top_10[ii]['COUNTRY']][0][0]/255, colourlists[top_10[ii]['COUNTRY']][0][1]/255, colourlists[top_10[ii]['COUNTRY']][0][2]/255, 1)
			cr.rectangle(10, (pos*100+90), 600+(800*(lengths[ii])), 60)
			cr.fill()

			ims2 = cairo.ImageSurface.create_from_png("flags/"+str(top_10[ii]['COUNTRY'])+".png")
			cr.set_source_surface(ims2, 13, (pos*100+95))
			cr.paint()

			#scoredisplay
			cr.move_to(55, (pos*100+135))
			cr.set_source_rgb(colourlists[top_10[ii]['COUNTRY']][2][0]/255, colourlists[top_10[ii]['COUNTRY']][2][1]/255, colourlists[top_10[ii]['COUNTRY']][2][2]/255)
			cr.show_text('#'+str(ii+1)+' '+name_list[str(top_10[ii]['NAME'])])
			cr.move_to(350, (pos*100+135))
			mins = '%01d' % (int(top_10[ii]['SCORE']/6000))
			secs = '%02d' % ((int(top_10[ii]['SCORE']/100))-int(mins)*60)
			hunds = '%02d' % (int(top_10[ii]['SCORE'])%100)
			cr.show_text(mins+":"+secs+":"+hunds)

			#date and title
			cr.set_font_size(55)
			cr.set_source_rgb(1, 1, 1)
			cr.move_to(1400, 60)
			cr.show_text(datetime.datetime.fromtimestamp(current_date).strftime('%Y-%m-%d'))
			cr.move_to(5, 60)
			cr.show_text(title)
			cr.set_font_size(35)


		frame=i*day_cycle+e
		ims.write_to_png("frames/image"+"%05d" % frame+".png")

with open('NF_NOEXPLOIT.json') as submissions:
	jeison = json.load(submissions)
	data = jeison[-1]['data']
#pick data for the track we will work on/excludes data we do not need
for i in range(len(data)):
	if data[i]['TRACK'] == track_select and data[i]['EXPIRED'] == '0':
		data[i]['SCORE'] = int(data[i]['SCORE'])
		data[i]['NAME'] = int(data[i]['NAME'])
		data[i]['UEC'] = int(data[i]['UEC'])
		data[i]['COUNTRY'] = int(data[i]['COUNTRY'])
		data[i]['DRIVER'] = int(data[i]['DRIVER'])
		data[i]['STYLE'] = int(data[i]['STYLE'])
		track_data.append(data[i])


track_data = sorted(track_data, key = lambda x: x['UEC'])

#determining start end and duration and other previously initialized values
start_date = track_data[0]['UEC']-(hour*12)
end_date = track_data[-1]['UEC']
duration = end_date - start_date + week
day_count = int(duration/hour/24)+3
week_count = int(day_count/7) 
#current_date = start_date - (day*5)
current_date = start_date-(day*5)

#starts a loop that lasts from arond the first submission in the category until the last.
for i in range(week_count):
	#for each submission ever in the track
	for entry in track_data:
		#sets ranktemp to be 11
		rank_temp = displayed_times+1
		#If the player had a previous time
		if entry['NAME'] in ranked_times:
			#if the previous time had a rank assigned to it. Needs to be checked in case it is the first submission of a player.
			if 'RANK' in ranked_times[entry['NAME']]:
				#save as the current rank of that player into a temporary variable, the rank of the previous time (needed soon to save it as previous rank)
				rank_temp = ranked_times[entry['NAME']]['RANK']
		#checks if the date of the time is within the bounds of the day currently worked on.
		if current_date < entry['UEC'] < (current_date + week):
			#if the entry of the player is already in the ranked times dict,
			if entry['NAME'] in ranked_times:
				#Confirms that the submission is indeed a PB. There are cases where this is not true.
				if ranked_times[entry['NAME']]['SCORE'] > entry['SCORE']:
					#replaces the entry in the ranked times dict
					ranked_times[entry['NAME']] = entry
					#adds the previously saved temp rank variable to the entry in ranked times list
					ranked_times[entry['NAME']]['RANK'] = rank_temp
			#If it was not a player ranked before, it simply adds the player to the list.
			else:
				#places the entry in the reanked times dict	
				ranked_times[entry['NAME']] = entry
				#adds the previously saved temp rank variable to the entry in ranked times list
				ranked_times[entry['NAME']]['RANK'] = rank_temp
	#clears top10
	top_10 = []
	#posts all the times from the dictionary into a list so they may be sorted.
	for entry in ranked_times:
		top_10.append(ranked_times[entry])
	#sorts the list of ranked times first by date and then by score
	top_10 = sorted(top_10, key = lambda x: x['UEC'])
	top_10 = sorted(top_10, key = lambda x: x['SCORE'])

	#updates the rank and prerank in the entries of the top_10
	for entry in range(len(top_10)):
		top_10[entry]['PRERANK']=top_10[entry]['RANK']
		top_10[entry]['RANK']=entry+1

	if len(top_10)<displayed_times:	
		for n in range(len(top_10)):
			print(name_list[str(top_10[n]['NAME'])]+' '+str(top_10[n]['SCORE'])+' rank: '+str(top_10[n]['RANK'])+' prev: '+str(top_10[n]['PRERANK'])+'Country: '+str(top_10[n]['COUNTRY']))
		displayed_length = len(top_10)
	else:
		for n in range(displayed_times):
			print(name_list[str(top_10[n]['NAME'])]+' '+str(top_10[n]['SCORE'])+' rank: '+str(top_10[n]['RANK'])+' prev: '+str(top_10[n]['PRERANK'])+'Country: '+str(top_10[n]['COUNTRY']))
		displayed_length = displayed_times
	print('\n')	
	old_top = top_10
	current_date+=week
	print(current_date)
	main()

		
	
