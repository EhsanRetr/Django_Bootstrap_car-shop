def user_Listing_path(instance, filename):
    return 'user_{0}/Listings/{1}'.format(instance.seller.user.id, filename)