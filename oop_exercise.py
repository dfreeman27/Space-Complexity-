class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.checked_out = False

        if not isinstance(year, int) or year <= 0:
            raise ValueError("Year must be a postive interger")

    def check_out(self):
        """Mark the book as checked out."""
        if self.checked_out:
            raise ValueError(f"The book '{self.title}' is already checked out.")
        self.checked_out = True

    def return_book(self):
        """Mark the book as returned."""
        if not self.checked_out:
            raise ValueError(f"The book '{self.title}' is not checked out.")
        self.checked_out = False

    def __repr__(self):
        status = 'Checked Out' if self.checked_out else 'Available'
        return f"'{self.title}' by {self.author} ({self.year}) - {status}"

class EBook(Book):
    """An electronic book that supports multiple checkouts."""

    def __init__(self, title, author, year, file_size_mb):
        super().__init__(title, author, year)

        self.file_size_mb = file_size_mb
        self.checkoutcount = 0

    def check_out(self):
        """Increment the number of active checkouts."""
        self.checkoutcount += 1

    def return_book(self):
        """Decrease the checkout count without going below zero."""
        if self.checkoutcount == 0:
            raise ValueError(
                f"The EBook '{self.title}' has no active checkouts."
            )

        self.checkoutcount -= 1

    def __repr__(self):
        return (
            f"'{self.title}' by {self.author} "
            f"({self.year}) - "
            f"File Size: {self.file_size_mb}MB, "
            f"Active Checkouts: {self.checkoutcount}"
        )


class Catalog:
    """Manages a collection of physical books and EBooks."""

    def __init__(self):
        self.books = []

    def add_book(self, book):
        """Add a Book or EBook to the catalog."""
        if not isinstance(book, Book):
            raise ValueError(
                "Only Book or EBook instances can be added."
            )

        self.books.append(book)

    def get_available_books(self):
        """Return all books available for checkout.

        Physical books must not already be checked out.
        EBooks remain available for multiple checkouts.
        """
        return [
            book for book in self.books
            if isinstance(book, EBook) or not book.checked_out
        ]

    def search_by_title(self, title):
        """Search for books by title, ignoring case."""
        return [
            book for book in self.books
            if title.lower() in book.title.lower()
        ]

    def search_by_author(self, author):
        """Search for books by author, ignoring case."""
        return [
            book for book in self.books
            if author.lower() in book.author.lower()
        ]

    def summary(self):
        """Display a summary of all books in the catalog."""
        total = len(self.books)

        checked_out = sum(
            1 for book in self.books
            if (
                book.checkoutcount > 0
                if isinstance(book, EBook)
                else book.checked_out
            )
        )

        print(
            f"\nCatalog Summary: "
            f"{checked_out}/{total} titles currently checked out."
        )

        for book in self.books:
            print(f" - {book}")
            