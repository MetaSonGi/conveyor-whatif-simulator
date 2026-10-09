"""다중 설비 공정에서 처리시간·병렬 대수·계획 정지 변경에 따른 대기시간과 처리량을 결정적으로 비교합니다."""
import argparse, json, math, html
from pathlib import Path

def finite(value, name, minimum=None):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(name + ': finite number required')
    if minimum is not None and value < minimum:
        raise ValueError(name + ': below minimum')
    return value

def report(result, title):
    payload=html.escape(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    return '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>body{font:16px/1.6 system-ui;max-width:1000px;margin:32px auto;padding:20px;background:#101b2b;color:#ecf4ff}pre{padding:24px;background:#192b40;border-radius:12px;white-space:pre-wrap;overflow-wrap:anywhere}h1{color:#80e4c5}</style><h1>'+html.escape(title)+'</h1><p>오프라인 샘플 계산 결과 · 실물 장비 연결 없음</p><pre>'+payload+'</pre></html>'

def cli(run,title):
    parser=argparse.ArgumentParser(description=title)
    parser.add_argument('--input',default=str(Path(__file__).with_name('sample-input.json')))
    parser.add_argument('--html',help='optional standalone HTML result path')
    args=parser.parse_args()
    try:
        data=json.loads(Path(args.input).read_text(encoding='utf-8'))
        result=run(data)
        if args.html: Path(args.html).write_text(report(result,title),encoding='utf-8')
        print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    except (ValueError,KeyError,TypeError) as exc:
        parser.exit(2, 'input error: '+str(exc)+'\n')

import heapq

def complete(start,duration,downtime):
    cursor=start;remaining=duration
    for begin,end in downtime:
        if end<=cursor:continue
        if begin>=cursor+remaining:return cursor+remaining
        if begin>cursor:remaining-=begin-cursor
        cursor=end
    return cursor+remaining

def simulate(jobs,stations):
    arrivals=[(finite(j['arrival_s'],'arrival_s',0),j['id']) for j in jobs]
    if len({j[1] for j in arrivals})!=len(arrivals):raise ValueError('duplicate job ID')
    if len({s['id'] for s in stations})!=len(stations):raise ValueError('duplicate station ID')
    logs=[];station_metrics=[]
    for s in stations:
        duration=finite(s['process_s'],'process_s',0)
        if duration<=0:raise ValueError('process_s must be positive')
        servers=s['servers']
        if type(servers) is not int or not 1<=servers<=1000:raise ValueError('servers must be integer 1..1000')
        downtime=[]
        for a,b in sorted(s.get('downtime',[])):
            finite(a,'downtime start',0);finite(b,'downtime end',0)
            if b<=a or downtime and a<downtime[-1][1]:raise ValueError('invalid/overlapping downtime')
            downtime.append((a,b))
        free=[(0,i) for i in range(servers)];heapq.heapify(free);output=[];waits=[]
        for arrival,job in sorted(arrivals):
            available,server=heapq.heappop(free);start=max(arrival,available)
            # Admission is delayed while a station is stopped; running jobs pause and resume.
            for a,b in downtime:
                if a<=start<b:start=b
            end=complete(start,duration,downtime);wait=start-arrival;waits.append(wait)
            logs.append({'job_id':job,'station_id':s['id'],'server':server,'arrival_s':arrival,'start_s':start,'end_s':end,'queue_wait_s':wait})
            heapq.heappush(free,(end,server));output.append((end,job))
        station_metrics.append({'station_id':s['id'],'average_queue_wait_s':round(sum(waits)/len(waits),6) if waits else 0})
        arrivals=output
    original={j['id']:j['arrival_s'] for j in jobs};makespan=max((a for a,_ in arrivals),default=0)
    return {'makespan_s':makespan,'throughput_per_minute':round(len(jobs)*60/makespan,6) if makespan else 0,
            'average_lead_time_s':round(sum(a-original[j] for a,j in arrivals)/len(jobs),6) if jobs else 0,
            'stations':station_metrics,'timeline':logs}

def run(data):
    if not data['baseline'] or not data['candidate']:raise ValueError('at least one station required')
    baseline=simulate(data['jobs'],data['baseline']);candidate=simulate(data['jobs'],data['candidate'])
    return {'baseline':baseline,'candidate':candidate,'makespan_saved_s':round(baseline['makespan_s']-candidate['makespan_s'],6),
            'assumptions':['unlimited_buffers','deterministic_process_times','preempt_resume_downtime','no_real_actuation']}

if __name__ == "__main__": cli(run,'컨베이어 공정 병목 비교기')
