#ifndef BOOTSTRAP_MANAGER_H
#define BOOTSTRAP_MANAGER_H

#include "libp2p/utils/vector.h"
#include "libp2p/multiaddress/multiaddress.h"
#include <pthread.h>
#include <time.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Struct representing a bootstrap peer entry
 */
struct BootstrapPeer {
    struct MultiAddress* address;   // Peer multiaddress
    time_t last_seen;               // Timestamp of last successful contact
};

/**
 * Manager for bootstrap peers
 */
struct BootstrapManager {
    struct Vector* peers;           // Vector of BootstrapPeer*
    pthread_mutex_t lock;           // Mutex for thread safety
    int max_peers;                  // Maximum number of peers to track
};

/**
 * Create a new BootstrapManager
 * @param max_peers maximum number of peers to track
 * @return pointer to BootstrapManager or NULL on failure
 */
struct BootstrapManager* bootstrap_manager_new(int max_peers);

/**
 * Free a BootstrapManager and its resources
 * @param mgr the BootstrapManager to free
 */
void bootstrap_manager_free(struct BootstrapManager* mgr);

/**
 * Add a peer to the manager
 * @param mgr the BootstrapManager
 * @param addr the MultiAddress of the peer
 * @return 1 on success, 0 on failure
 */
int bootstrap_manager_add_peer(struct BootstrapManager* mgr, struct MultiAddress* addr);

/**
 * Remove a peer from the manager
 * @param mgr the BootstrapManager
 * @param addr the MultiAddress of the peer to remove
 * @return 1 on success, 0 if not found
 */
int bootstrap_manager_remove_peer(struct BootstrapManager* mgr, struct MultiAddress* addr);

/**
 * Get a random peer from the manager
 * @param mgr the BootstrapManager
 * @return pointer to BootstrapPeer or NULL if empty
 */
struct BootstrapPeer* bootstrap_manager_get_random_peer(struct BootstrapManager* mgr);

/**
 * Update the last seen timestamp for a peer
 * @param mgr the BootstrapManager
 * @param addr the MultiAddress of the peer
 */
void bootstrap_manager_update_last_seen(struct BootstrapManager* mgr, struct MultiAddress* addr);

#ifdef __cplusplus
}
#endif

#endif /* BOOTSTRAP_MANAGER_H */
