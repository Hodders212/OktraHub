__context__ = "Selection"
__doc__ = "Filter Selection by choices"
__title__ = "Filter\nSelection"

from pyrevit import revit, DB, forms, script

def ListHeight(items):
	height = 185
	height += (len(items)*20)
	if height > 600:
		height = 600

	return height

selection = revit.get_selection()

filterList = ["Type", "Family", "Category", "Parameter Value", "Level", "Fitted",]

selectedFilter = forms.SelectFromList.show(
	filterList,
	title='Filter Selection By:',
	width=200,
	height=ListHeight(filterList),
	multiselect=False
)

if selectedFilter:
	if "Type" in selectedFilter:
		typeDictionary = {}

		for s in selection:
			try:
				typ_name = s.Symbol.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
				if typ_name in typeDictionary.keys():
					typeDictionary[typ_name] += [s]
				else:
					typeDictionary[typ_name] = [s]
			except:
				pass

		selectedFilter_type = forms.SelectFromList.show(
		typeDictionary.keys(),
		title='Filter Selection By:',
		width=400,
		height=ListHeight(typeDictionary.keys()),
		multiselect=True
		)

		final_selection = []
		if selectedFilter_type:
			for fibt in selectedFilter_type:
				for f in typeDictionary[fibt]:
					final_selection.append(f)

			selection.set_to(final_selection)

	elif "Family" in selectedFilter:
		familyDictionary = {}

		for s in selection:
			fam_name = "ITEM DOES NOT HAVE A FAMILY"
			try:
				fam_name = s.Symbol.FamilyName
			except:
				pass
			if fam_name in familyDictionary.keys():
				familyDictionary[fam_name] += [s]
			else:
				familyDictionary[fam_name] = [s]

		selectedFilter_family = forms.SelectFromList.show(
		familyDictionary.keys(),
		title='Filter Selection By:',
		width=400,
		height=ListHeight(familyDictionary.keys()),
		multiselect=True
		)

		if selectedFilter_family:
			final_selection = []
			for fibt in selectedFilter_family:
				for f in familyDictionary[fibt]:
					final_selection.append(f)
			selection.set_to(final_selection)

	elif "Category" in selectedFilter:
		categoryDictionary = {}

		for s in selection:
			cat_name = s.Category.Name
			if cat_name in categoryDictionary.keys():
				categoryDictionary[cat_name] += [s]
			else:
				categoryDictionary[cat_name] = [s]

		selectedFilter_category = forms.SelectFromList.show(
		categoryDictionary.keys(),
		title='Filter Selection By:',
		width=400,
		height=ListHeight(categoryDictionary.keys()),
		multiselect=True
		)

		final_selection = []
		if selectedFilter_category:
			for fibt in selectedFilter_category:
				for f in categoryDictionary[fibt]:
					final_selection.append(f)

			selection.set_to(final_selection)

	elif "Parameter Value" in selectedFilter:

		avail_params = []

		for s in selection:
			try:
				for sP in s.Parameters:
					avail_params += [sP.Definition.Name]
			except:
				pass
			try:
				for sP in s.Symbol.Parameters:
					avail_params += [sP.Definition.Name]
			except:
				pass

		filter_params = set(avail_params)

		param_list = forms.SelectFromList.show(
		sorted(filter_params),
		title='Filter Selection By:',
		width=400,
		height=ListHeight(filter_params),
		multiselect=False
		)

		if type(param_list) == str:
			param_list = [param_list]

		param_dict = {}

		for s in selection:
			param_val = "ERROR"
			try:
				param_param = s.LookupParameter(param_list[0])
				param_val_stor_typ = str(param_param.StorageType)

				if param_val_stor_typ == "String":
					param_val = param_param.AsString()
				elif param_val_stor_typ == "Double":
					param_val = param_param.AsDouble()
				elif param_val_stor_typ == "ElementId":
					param_val = param_param.AsElementId()
				else:
					param_val = param_param.AsInteger()
			except:
				try:
					param_param = s.Symbol.LookupParameter(param_list[0])
					param_val_stor_typ = str(param_param.StorageType)

					if param_val_stor_typ == "String":
						param_val = param_param.AsString()
					elif param_val_stor_typ == "Double":
						param_val = param_param.AsDouble()
					elif param_val_stor_typ == "ElementId":
						param_val = param_param.AsElementId()
					else:
						param_val = param_param.AsInteger()
				except:
					pass
			if param_val in param_dict.keys():
				param_dict[param_val] += [s]
			else:
				param_dict[param_val] = [s]

		selectedFilter_paramegory = forms.SelectFromList.show(
		sorted(param_dict.keys()),
		title='Filter Selection By:',
		width=400,
		height=ListHeight(param_dict.keys()),
		multiselect=True
		)

		if selectedFilter_paramegory:
			final_selection = []

			for fibt in selectedFilter_paramegory:
				for f in param_dict[fibt]:
					final_selection.append(f)

			selection.set_to(final_selection)

	elif "Level" in selectedFilter:
		
		levelDictionary = {}

		for s in selection:
			lvl_name = "Not Assigned to a Level"
			try:
				lvl_name = revit.doc.GetElement(s.LevelId).Name
			except:
				try:
					lvl_name = s.get_Parameter(DB.BuiltInParameter.PLAN_VIEW_LEVEL).AsString()
				except:
					pass

			if lvl_name in levelDictionary.keys():
				levelDictionary[lvl_name] += [s]
			else:
				levelDictionary[lvl_name] = [s]

		selectedFilter_type = forms.SelectFromList.show(
		levelDictionary.keys(),
		title='Filter Selection By:',
		width=400,
		height=ListHeight(levelDictionary.keys()),
		multiselect=True
		)

		final_selection = []

		for fibt in selectedFilter_type:
			for f in levelDictionary[fibt]:
				final_selection.append(f)

		selection.set_to(final_selection)

	elif "Fitted" in selectedFilter:
		
		filteredSelection = []

		for s in selection:
			try:
				s.LookupParameter("38mm WB").AsInteger()
				filteredSelection.append(s)
			except:
				pass

		selection.set_to(filteredSelection)