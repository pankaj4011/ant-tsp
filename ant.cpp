#include <bits/stdc++.h>
using namespace std;
typedef pair<int, int> pii;
#include "ant.hpp"
#include "graph.hpp"
const int inf = 1e9 + 7;

vector<pii> graph[100100];
vector<edge> edges;
int dist[1000][1000];
int adj[1000][1000];
double pheromone[1001][1001];
double lazy[1001][1001];
int n, m;

int src, dest;
void print(vector<int>& v) {
	for (auto x: v) {
		printf("%d ", x);
	}
	printf("\n");
}

void singlesource(int u) {
	for (int i = 1; i <= n; i++)
		dist[u][i] = inf;
	priority_queue<pii, vector<pii>, cmp> pq;
	dist[u][u] = 0;
	pq.push(make_pair(u, 0));
	while (!pq.empty()) {
		int v = pq.top().first, d = pq.top().second;
		pq.pop();
		for (auto p: graph[v]) {
			int nxt = p.first, w = p.second;
			if (dist[u][nxt] > dist[u][v] + w) {
				dist[u][nxt] = dist[u][v] + w;
				pq.push(make_pair(nxt, dist[u][nxt]));
			}
		}
	}
}


void allpairs() {
	for (int u = 1; u <= n; u++) {
		singlesource(u);
	}
}

int getnext(int from, bool* visited) {
	// gets probability distribution of which node to visit
	// next
	vector<pair<int, double> >prob;
	double sum = 0;
	for (auto i: graph[from]) {
		int vertex = i.first;
		if (visited[vertex] == 0) {
			double v = pheromone[from][vertex];
			sum += v;
			prob.push_back(make_pair(vertex, sum));
		}
	}

	int cnt = 0;
	for (auto i: graph[from]) {
		if (visited[i.first] == 0) {
			prob[cnt].second /= sum;
			if (from == src)
				printf("// prob %d -> %.2f\n", i.first, prob[cnt].second);
			cnt++;
		}
	}

	if (prob.empty())
		return -1;


	double r = rand() / (double) RAND_MAX;
	if (from == src)
	printf("// random number generated: %.2f\n", r);

	int ans;
	for (int i = 0; i < prob.size(); i++) {
		if (prob[i].second >= r) {
			ans = i;
			break;
		}
	}
	if (from == src)
	printf("// going to %d\n", prob[ans].first);
	return prob[ans].first;
}

int tour(vector<int>& path, int src, int dest) {
	bool visited[n + 1];
	memset(visited, 0, sizeof(visited));
	visited[src] = 1;
	int cnt = 1;
	int here = src;
	int len = 0; // length of tour
	while (here != dest) {
		path.push_back(here);
		int nxt = getnext(here, visited);
		if (nxt == -1) {
			return -1;
		}
		visited[nxt] = 1;
		len += adj[here][nxt];
		here = nxt;
		cnt++;
	}
	path.push_back(here);
	return len;
}

void evaporate() {
	double rho = 0.5; // decrease by factor of 0.4
	for (int i = 1; i <= n; i++) {
		for (int j = 1; j <= n; j++) {
			pheromone[i][j] = rho * pheromone[i][j];
		}
	}
}

int main(void) {
	srand(time(NULL));
	scanf("%d %d", &n, &m);
	for (int i = 1; i <= n; i++)
		for (int j = 1; j <= n; j++)
			pheromone[i][j] = 1.0;
	for (int i = 0; i < m; i++) {
		int u, v, w;
		scanf("%d %d %d", &u, &v, &w);
		graph[u].push_back(make_pair(v, w));
		graph[v].push_back(make_pair(u, w));
		edges.push_back(edge(u, v, w, 1.0));
		adj[u][v] = w;
		adj[v][u] = w;
	}
	scanf("%d %d", &src, &dest);
	allpairs();
	int ants = 100;
	int iter = 200;
	printf("%d %d\n", ants, iter);
	int mn = INT_MAX;
	vector<int> final_tour;
	while (iter--) {
		vector<int> paths[ants + 1];
		int lengths[ants + 1];
		// get every ant to tour
		for (int i = 0; i < ants; i++) {
			lengths[i] = tour(paths[i], src, dest);

			for (auto x: paths[i])
				printf("%d ", x);
			printf("\n");

			if (lengths[i] == -1) // no tour found
				continue;
			if (mn > lengths[i]) {
				final_tour.clear();
				for (auto x: paths[i])
					final_tour.push_back(x);
				mn = lengths[i];
			}
		}
		evaporate(); // evaporate pheromone from each edge by factor of 0.5

		// increase pheromones according to each ant
		for (int i = 0; i < ants; i++) {
			if (lengths[i] == -1)
				continue;
			for (int j = 0; j < paths[i].size() - 1; j++) {
				int u = paths[i][j], v = paths[i][j  + 1];
				pheromone[u][v] += 1.0 / lengths[i];
			}
		}
	}

	for (auto x: final_tour)
		printf("%d ", x);
	printf("\n");
}
