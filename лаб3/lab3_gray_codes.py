from collections import defaultdict
import itertools

class Hypercube:
    def __init__(self, n, k):
        self.n = n  # размерность
        self.k = k  # основание (алфавит {0, 1, ..., k-1})
        self.vertices = self._generate_vertices()
        self.graph = defaultdict(list)
        self._build_graph()
    
    def _generate_vertices(self):
        """Генерирует все вершины гиперкуба - векторы длины n над алфавитом {0,...,k-1}"""
        return list(itertools.product(range(self.k), repeat=self.n))
    
    def _build_graph(self):
        """Строит граф: ребро между вершинами, если отличаются ровно в одной координате"""
        for i, v1 in enumerate(self.vertices):
            for j, v2 in enumerate(self.vertices):
                if i < j:
                    diff = sum(1 for a, b in zip(v1, v2) if a != b)
                    if diff == 1:
                        self.graph[v1].append(v2)
                        self.graph[v2].append(v1)
    
    def get_vertex_degree(self, vertex):
        """Степень вершины = n(k-1)"""
        return self.n * (self.k - 1)
    
    def has_eulerian_cycle(self):
        """Эйлеров цикл существует, если все степени чётные"""
        degree = self.get_vertex_degree(self.vertices[0])
        return degree % 2 == 0
    
    def find_eulerian_cycle(self):
        """Находит эйлеров цикл алгоритмом на основе стека (алгоритм Флёри упрощённый)"""
        if not self.has_eulerian_cycle():
            return None
        
        # Копируем граф
        graph_copy = defaultdict(list)
        for v in self.graph:
            graph_copy[v] = self.graph[v].copy()
        
        # Начинаем с первой вершины
        start = self.vertices[0]
        stack = [start]
        cycle = []
        
        while stack:
            v = stack[-1]
            if graph_copy[v]:
                u = graph_copy[v].pop()
                graph_copy[u].remove(v)
                stack.append(u)
            else:
                cycle.append(stack.pop())
        
        return cycle[::-1]
    
    def find_eulerian_path(self):
        """Находит эйлеров путь (если цикла нет)"""
        # Для простоты используем тот же алгоритм
        graph_copy = defaultdict(list)
        for v in self.graph:
            graph_copy[v] = self.graph[v].copy()
        
        # Начинаем с первой вершины
        start = self.vertices[0]
        stack = [start]
        path = []
        
        while stack:
            v = stack[-1]
            if graph_copy[v]:
                u = graph_copy[v].pop()
                graph_copy[u].remove(v)
                stack.append(u)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    def is_hamiltonian(self, cycle):
        """Проверяет, является ли цикл гамильтоновым (посещает все вершины ровно 1 раз)"""
        if not cycle:
            return False
        # Проверяем, что все вершины различны (кроме первой и последней, если цикл)
        vertices_in_cycle = cycle[:-1] if cycle[0] == cycle[-1] else cycle
        return len(vertices_in_cycle) == len(set(vertices_in_cycle)) == len(self.vertices)
    
    def print_results(self):
        """Выводит результаты"""
        print(f"\n{'='*70}")
        print(f"ГИПЕРКУБ Q_{self.n}^{self.k}")
        print(f"{'='*70}")
        print(f"Количество вершин: {len(self.vertices)}")
        print(f"Степень вершины: {self.get_vertex_degree(self.vertices[0])}")
        print(f"Эйлеров цикл существует: {'ДА' if self.has_eulerian_cycle() else 'НЕТ'}")
        
        if self.has_eulerian_cycle():
            cycle = self.find_eulerian_cycle()
            print(f"Длина эйлерова цикла (рёбер): {len(cycle) - 1}")
            print(f"Цикл гамильтонов: {'ДА' if self.is_hamiltonian(cycle) else 'НЕТ'}")
            
            # Показываем первые 10 вершин цикла
            print(f"\nПервые 10 вершин цикла (код Грея):")
            for i, v in enumerate(cycle[:10]):
                print(f"  {i}: {v}")
            if len(cycle) > 10:
                print(f"  ... (всего {len(cycle)} вершин)")
            
            # Проверяем, что соседние отличаются в одной координате
            print(f"\nПроверка кода Грея (соседи отличаются в 1 координате):")
            all_valid = True
            for i in range(len(cycle) - 1):
                diff = sum(1 for a, b in zip(cycle[i], cycle[i+1]) if a != b)
                if diff != 1:
                    print(f"  ОШИБКА: между {cycle[i]} и {cycle[i+1]} разница = {diff}")
                    all_valid = False
            if all_valid:
                print("  ВСЕ СОСЕДИ ОТЛИЧАЮТСЯ В ОДНОЙ КООРДИНАТЕ - OK")
        else:
            path = self.find_eulerian_path()
            print(f"Эйлеров путь существует: ДА")
            print(f"Длина эйлерова пути (рёбер): {len(path) - 1}")


def main():

    # Тестовые случаи из задания
    test_cases = [
        (2, 2, "Бинарный гиперкуб (классический код Грея)"),
        (3, 2, "Бинарный гиперкуб n=3 (степень нечётная)"),
        (2, 3, "Троичный гиперкуб n=2 (степень чётная)"),
        (2, 4, "Четверичный гиперкуб n=2"),
        (3, 3, "Троичный гиперкуб n=3 (степень чётная)"),
    ]
    
    for n, k, description in test_cases:
        hc = Hypercube(n, k)
        hc.print_results()
        print(f"\nОписание: {description}")
        print("="*70)


if __name__ == "__main__":
    main()