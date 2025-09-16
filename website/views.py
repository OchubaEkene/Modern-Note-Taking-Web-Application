from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
import json
import logging
from flask_login import login_required, current_user
from .models import Note, User
from .forms import NoteForm, SearchForm
from . import db
from sqlalchemy import or_, and_

# Define a blueprint for the website
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """Main page with notes list and search functionality"""
    search_form = SearchForm()
    note_form = NoteForm()
    
    # Get search parameters
    query = request.args.get('query', '')
    category = request.args.get('category', '')
    show_favorites = request.args.get('favorites', False, type=bool)
    
    # Build query
    notes_query = Note.query.filter_by(user_id=current_user.id)
    
    if query:
        notes_query = notes_query.filter(
            or_(
                Note.title.contains(query),
                Note.content.contains(query)
            )
        )
    
    if category:
        notes_query = notes_query.filter_by(category=category)
    
    if show_favorites:
        notes_query = notes_query.filter_by(is_favorite=True)
    
    # Order by updated_at descending
    notes = notes_query.order_by(Note.updated_at.desc()).all()
    
    # Handle note creation
    if note_form.validate_on_submit():
        try:
            # Parse tags
            tags_list = []
            if note_form.tags.data:
                tags_list = [tag.strip() for tag in note_form.tags.data.split(',') if tag.strip()]
            
            new_note = Note(
                title=note_form.title.data,
                content=note_form.content.data,
                category=note_form.category.data,
                is_favorite=note_form.is_favorite.data,
                user_id=current_user.id
            )
            new_note.set_tags(tags_list)
            
            db.session.add(new_note)
            db.session.commit()
            flash('Note created successfully!', category='success')
            return redirect(url_for('views.home'))
        except Exception as e:
            logging.error(f"Error creating note: {str(e)}")
            db.session.rollback()
            flash('Error creating note. Please try again.', category='error')
    
    return render_template("home.html", 
                         user=current_user, 
                         notes=notes,
                         note_form=note_form,
                         search_form=search_form,
                         current_query=query,
                         current_category=category,
                         show_favorites=show_favorites)

@views.route('/note/<int:note_id>')
@login_required
def view_note(note_id):
    """View a specific note"""
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    return render_template("note_detail.html", note=note, user=current_user)

@views.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    """Edit a specific note"""
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    form = NoteForm(obj=note)
    
    if form.validate_on_submit():
        try:
            # Parse tags
            tags_list = []
            if form.tags.data:
                tags_list = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
            
            note.title = form.title.data
            note.content = form.content.data
            note.category = form.category.data
            note.is_favorite = form.is_favorite.data
            note.set_tags(tags_list)
            
            db.session.commit()
            flash('Note updated successfully!', category='success')
            return redirect(url_for('views.view_note', note_id=note.id))
        except Exception as e:
            logging.error(f"Error updating note: {str(e)}")
            db.session.rollback()
            flash('Error updating note. Please try again.', category='error')
    
    # Pre-populate tags field
    form.tags.data = ', '.join(note.get_tags())
    
    return render_template("edit_note.html", form=form, note=note, user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    """Delete a note via AJAX"""
    try:
        data = request.get_json()
        note_id = data.get('noteId')
        
        if not note_id:
            return jsonify({'error': 'Note ID is required'}), 400
        
        note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
        
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        db.session.delete(note)
        db.session.commit()
        
        return jsonify({'message': 'Note deleted successfully'})
    
    except Exception as e:
        logging.error(f"Error deleting note: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Error deleting note'}), 500

@views.route('/toggle-favorite/<int:note_id>', methods=['POST'])
@login_required
def toggle_favorite(note_id):
    """Toggle favorite status of a note"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
        
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        note.is_favorite = not note.is_favorite
        db.session.commit()
        
        return jsonify({
            'message': 'Favorite status updated',
            'is_favorite': note.is_favorite
        })
    
    except Exception as e:
        logging.error(f"Error toggling favorite: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Error updating favorite status'}), 500

@views.route('/api/notes')
@login_required
def api_notes():
    """API endpoint to get all notes as JSON"""
    try:
        notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).all()
        return jsonify([note.to_dict() for note in notes])
    except Exception as e:
        logging.error(f"Error fetching notes: {str(e)}")
        return jsonify({'error': 'Error fetching notes'}), 500


