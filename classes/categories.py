# categories API CRUD operations

from flask import request, jsonify, make_response
from app.models import Categories
from flask.views import MethodView
from classes.auth.auth import token_required
import re


class NonFilteredCategoryManipulations(MethodView):
    """This will handle the POST and Get methods with no parameters
    """

    decorators = [token_required]

    def post(self, user_in_session):
        """
       Create category
       ---
       tags:
         - Categories Endpoints
       parameters:
         - in: body
           name: Category details
           description: Create category by providing category name
           type: string
           required: true
           schema:
             id: create_categories
             properties:
               category_name:
                 default: Lunch
       responses:
         201:
           description: Category created successfully
         409:
           description: Category exists!
         400:
           description: Invalid category name given
         422:
           description: Please fill all the fields
        """
        categoryname = str(request.data.get('category_name', '')).strip()
        regexcategory_name = "[a-zA-Z0-9- .]"
        users_id = user_in_session
        category_exist = Categories.query.filter_by(users_id=user_in_session, category_name=categoryname).first()
        if categoryname:
            if re.search(regexcategory_name, categoryname):
                if not category_exist:
                    categories = Categories(category_name=categoryname, users_id=users_id)
                    categories.save()
                    return make_response(jsonify({'message': 'Category created successfully'})), 201
                return make_response(jsonify({'message': 'Category exists!'})), 409
            return make_response(jsonify({'message': 'Invalid category name given'})), 400
        return make_response(jsonify({'message': 'Please fill all the fields'})), 422

    def get(self, user_in_session):
        """
           Retrieve categories
           ---
           tags:
             - Categories Endpoints
           parameters:
             - in: query
               name: q
               description: Search parameter
               type: string

             - in: query
               name: page
               description: page number
               type: integer
               default: 1

             - in: query
               name: limit
               description: Limit
               type: integer
               default: 10

           responses:
             201:
               description: Category created successfully
             409:
               description: Category exists!
             400:
               description: Invalid category name given
             422:
               description: Please fill all the fields
        """
        try:
            page_number = int(request.args.get("page", default=1))
            no_items_per_page = int(request.args.get("limit", default=10))
        except Exception as e:
            return make_response(jsonify({"Error": "Not a valid page numbner or limit"})), 400

        if page_number <= 0 or no_items_per_page <= 0:
            page_number = 1
            no_items_per_page = 10

        number_of_categories = Categories.get_all(user_in_session).count()
        calculated_pages = int(number_of_categories/no_items_per_page)

        if page_number < calculated_pages:
            return make_response(jsonify({"Error": "Page not found"})), 404

        all_categories = Categories.get_all(user_in_session).paginate(page_number, no_items_per_page, error_out=False)
        search = request.args.get('q')
        category_list = []

        if search:
            searched_categories = Categories.query.filter(Categories.users_id == user_in_session,
                                                          Categories.category_name.ilike('%' + search + '%')).\
                paginate(page_number, no_items_per_page, error_out=False)

            if searched_categories:
                for categories in searched_categories.items:
                    obj = {
                            'id': categories.id,
                            'category_name': categories.category_name,
                            'user_id': categories.users_id,
                            'date_created': categories.created_at,
                            'date_updated': categories.updated_at
                            }
                    category_list.append(obj)
                if len(category_list) <= 0:
                    return make_response(jsonify({'message': "Category with the character(s) not found"})), 401
                return make_response(jsonify(category_list)), 200

        for categories in all_categories.items:
            obj = {
                'id': categories.id,
                'category_name': categories.category_name,
                'user_id': categories.users_id,
                'date_created': categories.created_at,
                'date_updated': categories.updated_at
            }
            category_list.append(obj)
        return make_response(jsonify(category_list)), 200


class FilteredCategoryManipulations(MethodView):
    """This will handle the GET, PUT and DELETE operations for a specific
        category filtered by ID
    """
    decorators = [token_required]

    def get(self, user_in_session, category_id):
        """
       Retrieve single category
       ---
       tags:
         - Categories Endpoints
       parameters:
         - in: path
           name: category_id
           description: category_id
           type: integer
       responses:
         401:
           description: Category not found
        """
        category = Categories.query.filter_by(id=category_id).first()
        if category:
            category_attributes = {
                'id': category.id,
                'category_name': category.category_name,
                'user_id': category.users_id,
                'date_created': category.created_at,
                'date_updated': category.updated_at
            }
            response = jsonify(category_attributes)
            response.status_code = 200
            return category_attributes
        return make_response(jsonify({'message': 'Category not found'})), 401

    def put(self, user_in_session, category_id):
        """
       Edit single category
       ---
       tags:
         - Categories Endpoints
       parameters:
         - in: path
           name: Category_id
           description: Category id
           type: integer
         - in: body
           name: category_name
           description: Category name
           type: string
       responses:
             201:
               description: Category updated successfully
             409:
               description: Category exists!
             400:
               description: Invalid category name given
             401:
               description: Category not found
             422:
               description: Please fill all the fields
        """
        category = Categories.query.filter_by(id=category_id).first()

        categoryname = str(request.data.get('category_name', '')).strip()
        regexcategory_name = "[a-zA-Z0-9- .]"
        category_existence = Categories.query.filter_by(category_name=categoryname).first()
        if category:
            if categoryname:
                if re.search(regexcategory_name, categoryname):
                    if not category_existence:

                        category.category_name = categoryname
                        category.save()

                        return make_response(jsonify({'message': 'Category updated successfully'})), 201
                    return make_response(jsonify({'message': 'Category exists!'})), 409
                return make_response(jsonify({'message': 'Invalid category name given'})), 400
            return make_response(jsonify({'message': 'Please fill all the fields'})), 422
        return make_response(jsonify({'message': 'Category not found'})), 401

    def delete(self, user_in_session, category_id):
        """
       Delete a category
       ---
       tags:
         - Categories Endpoints
       parameters:
         - in: path
           name: category_id
           description: category_id
           type: integer
       responses:
         200:
           description: Category deleted
         401:
           description: Category not found
        """
        category = Categories.query.filter_by(id=category_id).first()
        if category:
            category.delete()
            return make_response(jsonify({'message': 'Category deleted'})), 200
        return make_response(jsonify({'message': 'Category not found'})), 401


filtered_category = FilteredCategoryManipulations.as_view('filtered_category')
nonfiltered_category = NonFilteredCategoryManipulations.as_view('nonfiltered_category')
