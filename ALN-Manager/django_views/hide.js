function hide(some_node)
{
	some_node_classes = some_node.parentNode.parentNode;
	child_nodes=some_node_classes.childNodes;
	for(i=0; i<child_nodes.length; ++i){
		if(child_nodes[i].className==='classes') {
			if(child_nodes[i].style.display ==='none') {
				child_nodes[i].setAttribute('style', 'display: block;');
				some_node.innerHTML = 'collapse';
			} else {
				child_nodes[i].setAttribute('style', 'display: none;');
				some_node.innerHTML = 'expand';
			}
		}
	}
}

/**
 * Identifies the associated student div element for a particular
 * radio button and then adds the student to the chosen list then 
 * hiding the original student from the list.
 */
function select_student(selected_radio_button) {
	student_element = selected_radio_button.parentNode.parentNode;
	add_student(student_element);
}
		

/**
 * Identifies the associated class for a particular radio button 
 * and adds each of the students to the chosen list which have not 
 * already been added. Then the whole class is hidden
 */
function add_class(selected_radio_button)
{
	//removing the students
	this_class = selected_radio_button.parentNode.parentNode;
	this_class_children = this_class.getElementsByTagName('div');	
	the_students = this_class_children[1].getElementsByTagName('div'); //captures the contents of 'student_list'
	
	for(i=0; i<the_students.length; ++i) {
		if(the_students[i].className ==='student' && the_students[i].style.display !== 'none') {
			add_student(the_students[i]);
		}
	}
	
	//TODO: hiding the class element
	this_class_children[0].style.display = 'none';
}
	
/* Adds the selected student to the a list.
Currently only adds student no. to a list but should come up with
"selected students" div so action can be reversed. */
function add_student(student_element)
{
	student_id = (student_element.getAttribute('value'));
	list = document.getElementById('selected_students');
	new_list_item = document.createElement('li');
	new_list_item.innerHTML = student_id;
	list.appendChild(new_list_item);
	//list.appendChild(student_element);

	//hide the element in the list
	student_element.style.display = 'none';
}