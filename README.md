Для посадки дрона на платфору требуется разместить на ней 2 ArUco-маркера разных размеров.
Далее нужно указать размеры этих маркеров, в файле ~/catkin_ws/src/clever/clever/launch/clever.launch

# <param name="length_override/3" value="0.1"/>    <!-- маркер c id 3 имеет размер 10 см -->
# <param name="length_override/17" value="0.25"/>  <!-- маркер c id 17 имеет размер 25 см -->
 
 .
