<!DOCTYPE html>
<html>
	<head>
		<!-- metadata -->
		<meta charset="utf-8" />
		<meta name="author" content="SeoYeon Park" />
        <meta name="description" content="Capstone1" />
        <link rel="stylesheet" href="./Capstone1.css"/>
		<title>Data Civilizer</title>
	</head>

	<body>
		<h1>Design Log</h1>
		<ol>
		<li>profile은 pandas profiling을 사용한다: 10000개의 dataset을 가지고 검사를 했을 때 정확했고, 
			data civilizer를 구축하는데 필요한 profile 항목들이 들어있음. 결과적으로는 profiler를 구축하는데 걸리는 시간을 줄일 수 있음. <br> 
			이를 채택함으로써 샘플링 데이터를 가지고 프로파일 할 것인지와 single column profile에 대한 설계를 해결.  <br> 
			table에서 multiple columns profiling 과정도 해결</li>
		<li>Column유사성 계산: profile에 있는 데이터 빈도수를 바탕으로 (겹치는 데이터에서 작은 빈도수)/(전체 데이터의 합집합)으로 계산.</li>
		<li>IND: (칼럼간 교집합)/(FK 테이블의 칼럼 집합-중복 제거) == 1일 경우 PK에서 FK로의 IND가 성립</li>
		<li>arango db 채택: 파이썬 라이브러리 존재, 코드 공개 필요없는 라이센스.<br>* 네오포제이는 라이센스(bsd||apache||mit만 가능) 때문에 탈락, orient db는 디비 연결이 안되는 에러가 발생하여 진행 불가</li>
		</ol>
		<br><br>
		<h2>함수 설계</h2>
		<p>** 코딩 컨벤션: 스네이크 표기법 **</p>
		<ol>

			<li>Make DataBase & Polystore<br>
				Function makedb(char db, char file_name)<br>
				&nbsp;&nbsp;- db connect (host, user, password, db)<br>
				&nbsp;&nbsp;- csv 파일 읽어 db에 insert<br>
				Function polystore(char db)<br>
				&nbsp;&nbsp;- 필요한 데이터 select<br>
				&nbsp;&nbsp;- Numpy 형식으로 변환<br><br>
			</li>
			<li> Cleanliness<br>
				Function get_iqr (list data)<br>
				&nbsp;&nbsp;- q1, q3구해 -> iqr 구함<br>
				&nbsp;&nbsp;- 최소,최대 넘어가는 값들 보정/버리기<br>
				&nbsp;&nbsp;- Profiling할 data Numpy형식으로 저장<br><br>
			</li>
			<li> Profiling file <br>
				import file #2<br>
				A.   function profiling(list data)<br>
				&nbsp;&nbsp;- 앞에서 받아온 데이터를 가지고 profiling 진행<br>
				&nbsp;&nbsp;- Profiling result -> .json file로 생성<br>
				&nbsp;&nbsp;return .json file의 절대 경로(char) -> file 2-A로 넘겨줌<br><br>
			</li>
			<li> .json 파일 읽어와서 metadata 생성 및 IND/ col. 유사성 구하는 파일<br>
				import file #1<br>
				A.   function Select_Profile(char json파일 절대경로)<br>
				&nbsp;&nbsp;- .json에서 profiling 결과 읽어옴 + 필요한 profiling 결과만 추출<br>
				&nbsp;&nbsp;- 1-A의 리턴값 받아와서 json 파일 읽어옴<br>
				&nbsp;&nbsp;- profiling 결과 중 필요한 데이터만 추출<br>
				&nbsp;&nbsp;- 추출한 데이터 딕셔너리 형태로 가공<br>
				&nbsp;&nbsp;- 2-B에서 사용할 데이터(value_count, column name) list 형태로 저장<br>
				&nbsp;&nbsp;return select_profile(dictionary)<br>
				B.   function IND_ColSimilarity(list Col1, list Col2) # Col1&Col2 = 2-A에서 list형태로 저장한 데이터<br>
				&nbsp;&nbsp;return {IND: float value, col similarity: float value}<br>
				C.   function Combine_AB(dictionary A, dictionary B)<br>
				&nbsp;&nbsp;- input: 2-A와 2-B에서 만든 딕셔너리<br>
				&nbsp;&nbsp;- 2개의 딕셔너리 하나로 합치는 과정<br>
				&nbsp;&nbsp;return dictionary -> 최종적으로 update에 넘겨주는 데이터<br><br>
			</li>
			<li>update file <br>
				Function update<br>
				&nbsp;&nbsp;- dictionary 받아서 graphdb와 비교<br>
				&nbsp;&nbsp;- profiling 정보에서 max/min 값 비교<br>
				&nbsp;&nbsp;- 임계값 설정 (soft max)<br>
				&nbsp;&nbsp;- 초과하면 update<br>
				&nbsp;&nbsp;- make graphdb<br>
			</li>
		</ol>
		<br><br>
		<h1>Implementation Log</h1>
		<h2>08.28</h2>
		<p>
		1. 클리니스 한 결과, DB에 반영할 것인가? 아니면 데이터프레임에서만 삭제할 것인가?<br>
		&nbsp;&nbsp;-> 일단 데이터 프레임에서만 삭제<br>
		2. 유사성 계산후 프로파일링에 넘겨줄때 일단은 다 넘겨줌, 임계값 설정 필요<br>
		&nbsp;&nbsp;-> 일단은 임계값 설정 없이 진행<br>
		3. 아랑고 디비 키에 한글 입력 불가 : 노드 접근 용도이기 때문에 칼럼이 들어가야 함<br>
		&nbsp;&nbsp;-> 대부분의 디비 칼럼에는 영어를 사용함. 그렇기 때문에 테스트 파일의 칼럼 이름을 영어로 바꿀것<br>
		칼럼 유사성 -> type 비교로 수정: 칼럼 이름이 같을 경우만 검사했는데, type이 같을 경우 비교하는 것으로 수정할 것<br>
		<br>
		PyArango 사용할 경우,<br>
		1. collection(table) 생성시 각, 컬렉션 변수에 맞는 클래스 생성 해야함<br>
		&nbsp;&nbsp;그러나, 컬렉션 명을 변수로 넘겨주기 때문에 사실상 불가능<br>
		&nbsp;&nbsp;클래스를 생성하지 않는 경우 그래프 생성 불가능<br>
		&nbsp;&nbsp;그래프, 릴레이션 생성 역시 각 이름으로 된 클래스가 있어야 함<br>
		&nbsp;&nbsp;=> 1. github에 <a href="https://github.com/ArangoDB-Community/pyArango/issues/191" target="_blank">이슈</a> 올려볼 것 <br>
		&nbsp;&nbsp;&nbsp;2. 자바로 변경해서 해볼 것<br>
		</p>

		<h2>09.07</h2>
		<p>
		1. 설계 단계까지는 그래프의 노드가 의미하는 것이 테이블이었음, 구현과정에서 칼럼끼리 표시하는 것으로 바뀜<br>
		&nbsp;&nbsp;-> 어느것 채택? 일단은 칼럼으로 진행<br>
		2. 그래프 그리는것은 자바로 사용하면 될듯<br>
		&nbsp;&nbsp;자바 연결할 때 py4j 라이브러리 사용 -> bsd license<br>
		3. 아랑고디비에 컬렉션, 릴레이션, document추가 시 key값 중복이나, table exsists already 에러와 같은 것들 예외처리 수행<br>
		4. 추가 논의 사항<br>
		&nbsp;&nbsp;IND 화살표 방향 수정(PK-FK 관계)<br>
		&nbsp;1) py4j 라이브러리 사용 -> eclipse에서 자바를 실행시키는 과정이 필요해서 이 과정을 사용하지 않는 방법 찾는 중<br>
		&nbsp;&nbsp;&nbsp;&nbsp;: 자바에서 http 서버를 열어서 처리하는 방법<br>
		&nbsp;&nbsp;&nbsp;&nbsp;자바 apache http 설정 -> 자바를 runof로 사용: exec <br>
		&nbsp;&nbsp;&nbsp;&nbsp;-> 그냥 서버를 계속 띄워놓는게 나을듯, 매번 그래프를 그릴때마다 콜할 수는 없지 않나<br>
		&nbsp;2) 그래프의 노드가 의미하는 것이 원래는 테이블 이었으나 현재는 칼럼, 어느 것으로 해야하나? 현재 칼럼 쓰는 방법으로 사용<br>
		&nbsp;3) update에서 DB에서 업데이트 된 사항을 쿼리로그를 사용하여 선제적으로 처리하는 방법은 어떤가? 사용, 시스템프로그래밍 수업때 미니 쉘을 만들면서 history를 구현한 경험에서 착안하여
					키보드 화살표를 통해 이전에 실행한 쿼리를 가져올 수 있기 때문에, 이를 조회하는 기능이 있을것이라 생각했고
					쿼리 로그 기록을 알아내는 쿼리문을 찾음.<br>
					&nbsp;&nbsp;&nbsp;# 쿼리로그 기록 활성화 여부 확인<br>
					&nbsp;&nbsp;&nbsp;mysql> show variables like '%general%';<br>
					&nbsp;&nbsp;&nbsp;# 쿼리로그 기록 형식 확인<br>
					&nbsp;&nbsp;&nbsp;mysql> show variables like '%log_output%';<br>
					&nbsp;&nbsp;&nbsp;#general log 활성화<br>
					&nbsp;&nbsp;&nbsp;mysql> set global general_log=on;<br>
					&nbsp;&nbsp;&nbsp;#기록 형식 'TABLE'로 변경<br>
					&nbsp;&nbsp;&nbsp;mysql> set global log_output='TABLE';<br>
		&nbsp;4) 사용자가 원하는 데이터에 대한 쿼리를 던진 후 그 결과에 대해서는 어떠한 방식으로 보여주어야 하나?<br>
		&nbsp;&nbsp;&nbsp;&nbsp;그래프 비즈 사용 -> IND와 칼럼유사성은 구분하는 방식으로<br><br>
		** 폴리스토어에서 데이터프레임 넘길때 <br>
		-> 페이징작업해줄것(50개 또는 100개 잘라서 가져오기 1억건이면 100건씩 잘라서 여러번 가져오기
		전체 카운트 가져와서 몇개 가져올지 정하기)<br>
		그러면 1억건에 대해서 한번에 프로파일링을 하면? <br>
		&nbsp;&nbsp;&nbsp;&nbsp;터질 가능성이 아주 높음, 메모리 문제 <br>
		-> 증분 프로파일링 수행<br>
		=> 해보고 프로파일링 2개 비교해서 정확도 판단 다음에 논의<br>
		</p>

		<h2>09.28</h2>
		<p>
		1. 쿼리 로그 수정 <br>
		&nbsp;&nbsp;- 쿼리 로그에서 테이블 명 추출해서 집합 처리<br>
		&nbsp;&nbsp;- 이전 방식은 로그마다 프로파일링 진행했는데, 데이터가 10건 업데이트 되었다 했을때, 시스템에서 10번의 업데이트 진행<br>
		&nbsp;&nbsp;-> 한번만 진행하도록 쿼리 로그에서 테이블 명만 중복없이 추리는 작업 추가<br>
		2. 그래프 비즈 연동
		&nbsp;&nbsp;- 유사성은 직선, IND는 화살표 <br>
		3. 쿼리문 던졌을 때 그래프 띄어주기<br>
		4. 증분 프로파일링<br>
		&nbsp;&nbsp;table row 개수, missing value<br>
		&nbsp;&nbsp;column 별<br>
		&nbsp;&nbsp;&nbsp;- value_counts, distinct_count, type, max, min, range<br>
		&nbsp;&nbsp;&nbsp;- mean --> 평균적으로 0.02~0.03차이<br>
		5. 폴리스토어 페이징 작업<br>
		6. IND에서 PK-FK 관계 화살표 방향 정확하게 표시하기 <br>
		&nbsp;&nbsp;- from a to b: (a&b)/a == 1인 경우 IND, a가 FK b가 PK<br>
		&nbsp;&nbsp;- 논문에서 R[X]가 FK table이고 S[Y]가 PK table일 때 둘 사이에 IND가 성립할 때 이를 from R[X] -> to S[Y]라 나타냄<br>
		7. 클리니스<br>
		&nbsp;&nbsp;- 디비에 널값 -> 데이터 프레임으로 변환시 텍스트로 읽힘 -> 클리니스에서 결측값으로 재변경<br>
		8. 주기적으로 디비 로그 긁어오면서 사용자의 쿼리문 입력 항시 대기 -> multiprocessing으로 하고 싶은데 방법 찾는중<br>
		9. ArangoDB 그래프를 가져다 쓰지 않는다면, 자바를 연결하는 의미가 있나? 쿼리 던져서 가져오는데...<br>
		10. 페이징 작업시 한번에 몇개를 가져와야하나<br>
		11. 칼럼 유사성과 IND 계산 함수 분리<br>
		&nbsp;&nbsp;기존 방식에서는 한번에 계산. 그러나, 예를 들어 업데이트 과정에서 from과 to에 test1이 포함된 모든 릴레이션을 지우는데 이 과정에서 칼럼 유사성은 다시 업데이트 되지만
			test1이 PK인 경우를 계산하는 IND과정은 수행하지 않게 됨. 이를 해결하기 위해 test1을 from, to 각각 놓아 계산할 경우 칼럼 유사성에 대해 중복이 생김
			그래서, 함수를 분리하는 작업을 시행. 칼럼 유사성에서는 PK-FK 관계를 따지지 않음.(inter(col1, col2)/(col1+col2-inter(col1, col2)))<br>
		<br>
		**사용자에게 GraphViz를 사용하여 그래프를 띄우기 때문에 자바를 연결할 필요가 없어짐. 자바 연동 삭제<br>
		</p>

		<h2>11.04</h2>
		<p>
		어떤 텍스트가 들어오더라도 텍스트 연관성 분석 가능<br>
		유사문서검색, 워드 투 벡터 같은 알고리즘 찾아보기 + 유사 문서 검색<br>
		데이터에서 추출한 메타 정보를 가지고 데이터를 대표할 수 있는 키워드를 찾아냄<br>
		-> 상호 연관성분석 시 개런티 생기지 않을까<br>
		서로 다른 알고리즘 조사해서 각자 발표<br>
		데이터 성격에 따른 알고리즘 사용<br>
		: 어느 데이터 일때 어느 알고리즘 사용하는가<br>
		<br>
		수치형 데이터 - 사람 체온 데이터를 봤을때, 수치 제외하고 체온일 것이다라고 추정할 수 있는 사항<br>
		-> 비슷한 수치, 분포를 가지고 있지만 성격이 다른 것일 수도 있음, 그래서 어느 사항으로 추정할 지가 필요<br>
		+ 온도면 같은 로우에 사람 정보가 있음, 이것도 같이 봐서 추정<br>
		<br>
		그래서 텍스트에서도 유의미한 정보 추정 필요<br>
		<br>
		한컬럼 한컬럼을 어떻게 할지에서 시작해서<br>
		하나의 테이블 안에서 여러 레코드를 다 모았을 때 텍스트의 양은 많음, 이때 이 텍스트들을 어떻게 분석할 것인가,<br>
		어떤 알고리즘을 사용할 것인가, 모았을 때 주요 키워드를 어떻게 뽑아낼것인가.<br>
		<br>
		</p>

		<h2>11.19</h2>
		<p>
		지금까지 했던 여러 방식들을 활용<br>
		온톨로지 기반<br>
		수많은 데이터에서 메타 데이터 추출해서 유사하거나 상관관계가 있다고 판별되면 데이터끼리 연관시켜 나가는것이 온톨로지<br>
		그럼 메타정보를 어떻게 뽑아야 하는가? 텍스트, 숫자에 대해서는 준비를 해놨음(다른 자료형에대해서는 또다른 준비 필요)<br>
		온톨로지가 구축이 되어있다는 전제하에 온톨로지를 활용해서 input으로 넣었던 데이터를 다 넣어서 온톨로지와 비교해서<br>
		어느 데이터와 무엇이 비슷한지 뽑아내기<br>
		</p>

	<h2>중간보고</h2>
	<p>
	<a href="https://github.com/nsa32752/2020-2/tree/main/Capstone1" target="_blank">중간보고서 및 발표영상</a>
	</p>
</body>

</html>
